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

    command = ["ffmpeg", "-i", inputfile]
    if 'bitrate' in options:
        command.append("-ab")
        command.append(options['bitrate'].replace(" kbps", "k"))
    
    if 'frequency' in options:
        command.append("-ar")
        command.append(options['frequency'].replace(" hz", ""))

    if 'channels' in options:
        if options['channels'] == "mono":
            command.append("-ac")
            command.append("1")
        if options['channels'] == "stereo":
            command.append("-ac")
            command.append("2")
    
    if 'audio_start' in options['trim'] and 'audio_end' in options['trim']:
        command.append("-ss")
        command.append(options['trim']['audio_start'])
        command.append("-to")
        command.append(options['trim']['audio_end'])

    command.append("-strict")
    command.append("-2")
    command.append(outputfile)
    command.append("-y")
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
