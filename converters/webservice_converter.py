import os
import uuid
from flask import json
import subprocess
import boto3
import shutil
import re

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
    inputfile = os.path.join(config['UPLOAD_DIR'], file_object['path'])
    dest_format = "mp4"

    command = ["ffmpeg", "-i", inputfile]

    if 'size' in options:
        size = options['size']

        width = 0
        height = 0
        fps = 30

        result = re.findall("(\d+)x(\d+)", size)
        if(len(result) == 1):
            width, height = result[0]
        
        result = re.findall("(\d+)p", size)
        if(len(result) == 1):
            width = result[0]
        
        result = re.findall("(\d+)fps", size)
        if(len(result) == 1):
            fps = result[0]
        
        command += ["-vf"]
        if height == 0:
            command += ["scale='%s:-2'" % (width)]
        else:
            command += ["scale='%s:%s'" % (width, height)]
        
        command += ["-r", str(fps)]


    if 'video_start' in options['trim'] and 'video_end' in options['trim']:
        command.append("-ss")
        command.append(options['trim']['video_start'])
        command.append("-to")
        command.append(options['trim']['video_end'])

    if options['disableAudio'] == True:
        command.append("-an")

    outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
    
    command.append(outputfile)
    command.append("-y")
    subprocess.call(command)

    #upload to s3
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
