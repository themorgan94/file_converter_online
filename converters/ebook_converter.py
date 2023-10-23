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
            'message': 'Unable to convert some files due to server issue or give file was invalid, please try again',
            'results': []
        }


def convert_each(file_object, dest_format, options, config):
    outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
    inputfile = os.path.join(config['UPLOAD_DIR'], file_object['path'])

    command = ["ebook-convert", inputfile, outputfile]

    if 'target' in options:
        command.append("--output-profile")
        command.append(options['target'])
    
    if 'title' in options and options['title']:
        command.append("--title")
        command.append(options['title'])

    if 'author' in options and options['author']:
        command.append("--authors")
        command.append(options['author'])

    if 'font' in options and options['font']:
        command.append("--base-font-size")
        command.append(options['font'])

    if 'encoding' in options:
        command.append("--input-encoding")
        command.append(options['encoding'].split(" ")[0].lower())

    if 'encoding' in options:
        command.append("--input-encoding")
        command.append(options['encoding'].split(" ")[0].lower())

    if 'ascii' in options and options['ascii'] == True:
        command.append("--asciiize")
    
    if 'heuristics' in options and options['heuristics'] == True:
        command.append("--enable-heuristics")


    subprocess.call(command)

    s3 = boto3.client('s3')
    object_name = os.path.join(os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
    if config['LOCAL']:
        return object_name
        
    response = s3.upload_file(
        outputfile, 
        config['BUCKET'], 
        object_name
    )

    shutil.rmtree(os.path.dirname(outputfile))
    return s3.generate_presigned_url('get_object', ExpiresIn=86400, Params={'Bucket': config['BUCKET'], 'Key': object_name})
