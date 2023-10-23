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
        command.append("-vb")
        command.append(options['bitrate'] + "k")
    
    if 'framerate' in options:
        command.append("-filter:v")
        command.append("fps=fps={}".format(options['framerate']))

    if 'flip' in options:
        command.append("-vf")
        if options['flip'] == "Horizontally":
            command.append("hflip")
        if options['flip'] == "Vertically":
            command.append("vflip")

    if 'rotate' in options:
        command.append("-vf")
        if options['rotate'] == "90":
            command.append("\"transpose=1\"")
        if options['rotate'] == "180":
            command.append("\"transpose=1,transpose=1\"")
        if options['rotate'] == "270":
            command.append("\"transpose=1,transpose=1\"")
    
    if 'video_start' in options['trim'] and 'video_end' in options['trim']:
        command.append("-ss")
        command.append(options['trim']['video_start'])
        command.append("-to")
        command.append(options['trim']['video_end'])

    if dest_format.lower() in ["3gp", "3g2"]:
        command = command +  ["-r","20","-s","352x288","-vb","400k","-acodec","aac","-strict","experimental","-ac","1","-ar","8000","-ab","24k"]

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
