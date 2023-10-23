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
    inputfile = os.path.join(config['UPLOAD_DIR'], file_object['path'])

    command = ["ffmpeg", "-i", inputfile]

    if(dest_format.lower() in ["android", "ipone", "ipad", "ipod"]):
        command += ["-c:v", "libx264", "-c:a", "aac", "-movflags", "+faststart"]

        if "size" in options:
            command += ["-s", options['size']]
        dest_format = "mp4"
    

    if(dest_format.lower() == "blackberry"):
        command += ["-f", "mp4", "-aspect", "2.409", "-vcodec", "libx264", "-s", "480x200", "-r", "24", "-b", "220k", "-acodec", "libmp3lame", "-ab", "24kbit/s", "-ac" ,"1","output.mp4"]
        dest_format = "mp4"
    
    if(dest_format.lower() == "blackberry"):
        command += ["-f", "mp4", "-aspect", "2.409", "-vcodec", "libx264", "-s", "480x200", "-r", "24", "-b", "220k", "-acodec", "libmp3lame", "-ab", "24kbit/s", "-ac" ,"1","output.mp4"]
        dest_format = "mp4"

    if(dest_format.lower() == "playstation"):
        command += ["-crf", "22"]
        dest_format = "mp4"

    if(dest_format.lower() == "psp"):
        command += ["-flags", "+bitexact", "-vcodec", "libx264", "-profile:v", "baseline", "-level", "3.0", "-s", "480x272", "-r", "29.97", "-b:v", "384k", "-acodec", "aac", "-b:a", "96k", "-ar", "48000", "-f", "psp", "-strict", "-2"]
        dest_format = "mp4"

    if(dest_format.lower() == "wii"):
        command += ["-vf", "scale='512:-1'", "-r", "29.97", "-c:v", "mjpeg", "-acodec", "pcm_s16le"]
        dest_format = "avi"

    if(dest_format.lower() == "xbox"):
        command += ["-c:v", "libx264", "-profile:v", "high", "-crf", "23", "-c:a", "libfaac", "-q:a", "100"]
        dest_format = "mp4"


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
