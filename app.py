import os
from flask import Flask, make_response, request, flash, render_template, json, redirect, url_for, abort, session, g
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse

import uuid
from rq import Queue
from rq.job import Job
from worker import conn
import boto3
import time
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

from converters import image_converter, \
    audio_converter, video_converter, \
        document_converter, archive_converter, \
            ebook_converter, device_converter, webservice_converter, \
                pdf_converter, documents_compressor, image_compressor, \
                    video_compressor

from apscheduler.schedulers.background import BackgroundScheduler
from schedular import expire_files
from flask_babel import Babel, gettext as  _
from flask_minify import minify


sched = BackgroundScheduler(daemon=True)
sched.add_job(expire_files,'interval',minutes=60)
sched.start()

app = Flask(__name__)
app.secret_key = 'super secret key'

dir_path = os.path.dirname(os.path.realpath(__file__))

CONFIG_FOLDER = os.path.join(dir_path, "configs")

app.config['UPLOAD_DIR'] = os.path.join(dir_path, "static", "uploads")
app.config['BUCKET'] = os.getenv("aws_bucket")
app.config['LOCAL'] = False

if app.config['BUCKET'] is None:
    app.config['LOCAL'] = True

babel = Babel(app)
minify(app=app, html=True, js=True, cssless=True)


q = Queue(connection=conn)

convert_list = {
    "image": image_converter,
    "audio": audio_converter,
    "video": video_converter,
    "document": document_converter,
    "archive": archive_converter,
    "ebook": ebook_converter,
    "device": device_converter,
    "webservice": webservice_converter,
    "pdf": pdf_converter,
    "document-compressor": documents_compressor,
    "image-compressor": image_compressor,
    "video-compressor": video_compressor
}

from configs.filetypes import available_filetypes
from configs.definition import definitions
from configs.languages import supported_languages

@babel.localeselector
def get_locale():
    return "en" if not g.lang_code \
        else g.lang_code

@app.route('/switch-language/<lang>')
def swith_language(lang):
    if lang in supported_languages.keys():
       g.lang_code = lang

    if request.referrer:
        path = replace_url_lang(request.referrer, lang)
        return redirect(
            path
        )
    else:
        return redirect("/")

def replace_url_lang(url, lang, full=False):
    path = url_parse(url).path
        
    paths = path.split("/")
    paths.pop(0)

    if len(paths) > 0 and paths[0] in supported_languages.keys():
        prev = "/" + paths[0]
        next = "/" + lang

        path = path.replace(prev, next if lang != "en" else "")
    
    elif lang != "en":
        path = "/" + lang + path
    
    return path if not full else request.url_root.rstrip("/") + path

@app.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code

@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if values is not None and 'lang_code' in values:
        lang_code = values.pop('lang_code', None)

        if lang_code in supported_languages.keys() and lang_code != "en":
            g.lang_code = lang_code
        else:
            abort(404)
    else:
        g.lang_code = "en"

@app.route("/<lang_code>")
@app.route("/<lang_code>/")
@app.route("/")
def index():
    return render_template('index.html', filetypes = available_filetypes)


@app.route('/converter/<filetype>', methods = ['GET'])
@app.route("/<lang_code>/converter/<filetype>", methods = ['GET'])
@app.route('/converter/<filetype>/<fileformat>', methods = ['GET', 'POST'])
@app.route('/<lang_code>/converter/<filetype>/<fileformat>', methods = ['GET', 'POST'])
def converter(filetype, fileformat=None):
    if fileformat == None:
        return render_template('list.html', 
                filetypes = available_filetypes,
                filetype = filetype,
                fileformat = fileformat
                )

    if request.method == "GET":
        return render_template('converter.html', 
                filetypes = available_filetypes,
                filetype = filetype,
                fileformat = fileformat,
                options= json.dumps(available_filetypes[filetype]['options'], sort_keys = False, indent = 2)
                )
    else:
        urls = request.form.getlist('url[]')
        if len(urls) == 0:
            flash(_("Please upload a file to convert."), "error")
            return redirect(
                url("/converter/{}/{}".format(filetype, fileformat))
            )
        if len(urls) >= 10:
            flash(_("Sorry! currently we only support 10 files batch."), "error")
            return redirect(
                url("/converter/{}/{}".format(filetype, fileformat))
            )


        job = q.enqueue_call(
                func=convert_list[filetype].convert, 
                args=(urls, 
                        fileformat,
                        json.loads(request.form.get('options')),
                        {
                            "UPLOAD_DIR": app.config['UPLOAD_DIR'],
                            "BUCKET": app.config['BUCKET']
                        }
                        ), 
                result_ttl=5000,
                timeout=500
            )

        return redirect(
            url("/output/{}".format(job.get_id()))
        )

@app.route('/<lang_code>/output/<job_id>', methods = ['GET'])                
@app.route('/output/<job_id>', methods = ['GET'])
def output(job_id):
    try:
        job = Job.fetch(job_id, connection=conn)
        return render_template('output.html', job = job, job_id= job_id)
    except:
        abort(404)

@app.route('/job/status/<job_id>', methods = ['GET'])
def jobStatus(job_id):
    try:
        job = Job.fetch(job_id, connection=conn)
        response = app.response_class(
            response = json.dumps({
                'is_finished': job.is_finished,
                'is_failed': job.is_failed,
                'is_queued': job.is_queued,
                'is_started': job.is_started
            }),
            status=200,
            mimetype='application/json'
        )
        return response
    except:
        abort(404)

@app.route('/<lang_code>/formats')
@app.route('/formats')
def formats():
    types = {}
    q = request.args.get("q")
    if q == None:
        q = ""
        
    for filetype in available_filetypes:
        for ext in available_filetypes[filetype]['ext']:
            if q != None and \
                (
                    q.lower() in ext.lower() or 
                    q.lower() in definitions[ext]
                ):
                types[ext] = {
                    "type": filetype,
                    "def" : definitions[ext] 
                }
            elif(q == None):
                types[ext] = {
                    "type": filetype,
                    "def" : definitions[ext] 
                } 
    return render_template('formats.html', types = types, q = q)

@app.route('/upload', methods = ['POST'])
def upload():
    files = request.files.getlist('files')
    filenames = []
    for file in files:
        filename = secure_filename(file.filename)
        n, e = os.path.splitext(filename)

        filename = n + e.lower()

        folder =  uuid.uuid4().hex

        os.makedirs(os.path.join(app.config['UPLOAD_DIR'], folder), exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_DIR'], folder , filename))

        filenames.append({
            "path" : os.path.join(folder, filename),
            "name" : n,
            "ext"  : e
        })

    response = app.response_class(
        response=json.dumps({
            'success': True,
            'files': filenames
        }),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/upload/remove', methods = ['GET'])
def remove_folder():
    path = request.args.get('fileid')
    if path and len(path) != 0 \
        and os.path.exists(os.path.join(app.config['UPLOAD_DIR'], path)):
        os.remove(os.path.join(app.config['UPLOAD_DIR'], path))
    return "ok"

@app.route("/<lang_code>/disclaimer")
@app.route('/disclaimer')
def disclaimer():
    return render_template("disclaimer.html")

@app.route("/<lang_code>/privacy")
@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route("/<lang_code>/about")
@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/<lang_code>/faq")
@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route("/sitemap")
@app.route("/sitemap/")
@app.route("/sitemap.xml")
def sitemap():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    for rule in ["/", "/about", "/blogs", "/formats", "/faq", "/privacy"]:
        url = {
            "loc": f"{host_base}{str(rule)}"
        }
        static_urls.append(url)
    
    for filetype, fileinfo in available_filetypes.items():
        url = {
                "loc": f"{host_base}/converter/{filetype}",
            }
        static_urls.append(url)
        for ext in fileinfo['ext']:
            url = {
                "loc": f"{host_base}/converter/{filetype}/{ext}",
            }
            static_urls.append(url)

    xml_sitemap = render_template("sitemap.xml", static_urls=static_urls, dynamic_urls=[], host_base=host_base)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response

@app.template_filter('basename')
def basename(s):
    return os.path.basename(s)

@app.template_filter('splitpart')
def splitpart (value, index, char = ','):
    return value.split(char)[index]

def url(path):
    if g.lang_code == "en":
        return path
    return "/" + g.lang_code + path

@app.context_processor
def functions():
    def get_definitions():
        return definitions

    def get_types():
        return available_filetypes

    return {
        "definitions": get_definitions,
        "available_types": get_types,
        "config": app.config,
        "url_for": url_for,
        "url" : url,
        "join": os.path.join,
        "supported_languages": supported_languages,
        "replace_url_lang": replace_url_lang,
        "current_url": request.url
    }

if __name__ == "__main__":
    app.run(debug=True)