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
    dest_format = dest_format.split("_")[0]
    file_object['name'] += "_compressed"

    outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
    inputfile = os.path.join(config['UPLOAD_DIR'], file_object['path'])

    command = ["clear"]
    if dest_format.lower() in ["mp4"]:
        command = ["ffmpeg","-y", "-i", inputfile,"-vcodec","h264","-b:v","250k","-acodec","mp3", outputfile]

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
