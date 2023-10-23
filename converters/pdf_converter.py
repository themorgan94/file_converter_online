import os
import uuid
from flask import json
import subprocess
import boto3
import shutil
from pdf2image import convert_from_path, convert_from_bytes
import img2pdf


def convert(file_paths, dest_format, options, config):
    try: 
        if dest_format.lower() == "images-to-pdf":
            results = convert_each(file_paths, dest_format, options, config)
        elif dest_format.lower() == "pdf-to-images":
            results = [convert_each(json.loads(file_path), dest_format, options, config) for file_path in file_paths]
        
        return {
            'error': False,
            'results': results
        }
    except Exception as e:
        return {
            'error': True,
            'message': 'Unable to convert some files due to server issue or give file was invalid, please try again',
            'results': []
        }

def convert_each(file_object, dest_format, options, config):
    if dest_format.lower() == "pdf-to-images":
        inputfile = os.path.join(config['UPLOAD_DIR'], file_object['path'])

        outputFolder = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']))

        images = convert_from_path(inputfile)
        dest_format = "zip"

        #save images
        files = []
        for idx, image in enumerate(images):
            filename = os.path.join(outputFolder, "image_%i.jpg" % (idx))
            image.save(filename)
            files.append(filename)

        outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
        
        #compress to zip
        command = ["7za", "a", outputfile] + files
        subprocess.call(command)

        object_name = os.path.join(os.path.dirname(file_object['path']), file_object['name'] + ".zip")


    elif dest_format.lower() == "images-to-pdf":
        files = []
        for _file_object in file_object:
            _file_object = json.loads(_file_object)
            
            inputfile = os.path.join(config['UPLOAD_DIR'], _file_object['path'])
            subprocess.call(
                ["convert", inputfile, "-background", "white", "-alpha", "remove", "-alpha", "off", inputfile]
            )
            files.append(inputfile)

        outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(_file_object['path']), "pdf_{}".format(uuid.uuid4().hex[0:5])) + ".pdf"
        
        with open(outputfile,"wb") as f:
	        f.write(img2pdf.convert(files))

        object_name = os.path.join(os.path.dirname(_file_object['path']), _file_object['name'] + ".pdf")
    
    if config['LOCAL']:
        return object_name
        
    #upload to s3
    s3 = boto3.client('s3')
    response = s3.upload_file(
        outputfile, 
        config['BUCKET'], 
        object_name
    )
    
    if dest_format.lower() == "images-to-pdf":
        for _file_object in file_object:
            _file_object = json.loads(_file_object)
            shutil.rmtree(os.path.join(config['UPLOAD_DIR'], os.path.dirname(_file_object['path'])))
        return [s3.generate_presigned_url('get_object', ExpiresIn=86400, Params={'Bucket': config['BUCKET'], 'Key': object_name})]
    else:
        shutil.rmtree(os.path.dirname(outputfile))
        return s3.generate_presigned_url('get_object', ExpiresIn=86400, Params={'Bucket': config['BUCKET'], 'Key': object_name})
