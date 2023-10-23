import os
import uuid
from flask import json
import subprocess
import boto3
import shutil

def convert(file_paths, dest_format, options, config):
    try: 
        return {
            'error': False,
            'results': [convert_each(json.loads(file_path), dest_format, options, config) for file_path in file_paths]
        }
    except Exception as e:
        return {
            'error': True,
            'message': e, #'Unable to convert some files due to server issue or give file was invalid, please try again',
            'results': []
        }


def convert_each(file_object, dest_format, options, config):
    outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
    inputfile = os.path.join(config['UPLOAD_DIR'], file_object['path'])

    if file_object['ext'] in [".pdf"] and dest_format.lower() in ['doc', 'docx']:
        command = ["pdf2docx","convert", inputfile, outputfile, "--multi_processing=True"]
    
    elif file_object['ext'] in [".ppt", ".pptx"] and dest_format.lower() in ['doc', 'docx']:
        if file_object['ext'] in [".ppt", ".pptx"]:
            subprocess.call(["unoconv", "-f", "pdf", "-o", outputfile.replace(dest_format.lower(), "pdf"), inputfile])
        command = ["pdf2docx","convert", inputfile.replace(file_object['ext'], ".pdf"), outputfile, "--multi_processing=True"]
    

    elif file_object['ext'] in [".xls", ".xlsx"] and dest_format.lower() in ['doc', 'docx', 'odt']:
        subprocess.call(["unoconv", "-f", "pdf",   "-o", outputfile.replace(dest_format.lower(), "pdf"), inputfile])
        command = ["pdf2docx","convert", inputfile.replace(file_object['ext'], ".pdf"), outputfile, "--multi_processing=True"]
    
    elif file_object['ext'] in [".pdf"] and dest_format.lower() in ['html']:
        subprocess.call(["pdf2docx","convert", inputfile, outputfile.replace(dest_format.lower(), "doc")])
        command = ["unoconv", "-f", "html",   "-o", outputfile, inputfile.replace(file_object['ext'], ".doc")]
    
    elif dest_format.lower() in ['pptx', 'ppt']:
        if file_object['ext'] not in [".pdf"]:
            subprocess.call(["unoconv", "-f", "pdf", "-o", outputfile.replace(dest_format.lower(), "pdf"), inputfile])
        command = ["pdf2pptx", inputfile.replace(file_object['ext'], ".pdf")]
        subprocess.call(command)
        if dest_format.lower() in ['ppt']:
            os.rename(outputfile.replace(dest_format.lower(), "pptx"), outputfile)
        command = ["clear"]
    
    elif dest_format.lower() in ['rtf', 'txt', 'odt']:
        if file_object['ext'] in [".xls", ".xlsx", ".ppt", ".pptx", ".rtf", ".odt", ".doc", ".docx"]:
            subprocess.call(["unoconv", "-f", "pdf",   "-o", outputfile.replace(dest_format.lower(), "pdf"), inputfile])
            subprocess.call(["pdf2docx","convert", inputfile.replace(file_object['ext'], ".pdf"), outputfile.replace(dest_format.lower(), "docx"), "--multi_processing=True"])
        elif file_object['ext']  == ".pdf":
            subprocess.call(["pdf2docx","convert", inputfile, outputfile.replace(dest_format.lower(), "docx"), "--multi_processing=True"])
        else:
            subprocess.call(["unoconv", "-f", "docx",   "-o", outputfile.replace(dest_format.lower(), "docx"), inputfile])
            
        command = ["unoconv", "-f", dest_format.lower(), "-o", outputfile, inputfile.replace(file_object['ext'], ".docx")]
    
    else:
        command = ["unoconv", "-f", dest_format.lower(), "-o", outputfile, inputfile]
    subprocess.call(command)
    
    object_name = os.path.join(os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
    if config['LOCAL']:
        return object_name

    s3 = boto3.client('s3')
    response = s3.upload_file(
        outputfile, 
        config['BUCKET'], 
        object_name
    )

    shutil.rmtree(os.path.dirname(outputfile))
    return s3.generate_presigned_url('get_object', ExpiresIn=86400, Params={'Bucket': config['BUCKET'], 'Key': object_name})
