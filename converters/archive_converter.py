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
            'results': convert_each(file_paths, dest_format, options, config)
        }
    except Exception as e:
        return {
            'error': True,
            'message': 'Unable to convert some files due to server issue or give file was invalid, please try again',
            'results': []
        }


def convert_each(file_objects, dest_format, options, config):
    files = []
    for file_object in file_objects:
        file_object = json.loads(file_object)
        
        inputfile = os.path.join(config['UPLOAD_DIR'], file_object['path'])
        files.append(inputfile)
   
    outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']), "archive_{}".format(uuid.uuid4().hex[0:5]))

    if dest_format == "TAR.GZ":
        command = ["7za", "a", outputfile + ".tar"] + files 
        subprocess.call(command)
        command = ["7za", "a", outputfile+".tgz", outputfile +".tar"]
        subprocess.call(command)
        dest_format = "tgz"
    if dest_format == "TAR.BZ2":
        command = ["7za", "a", outputfile + ".tar"] + files 
        subprocess.call(command)
        command = ["7za", "a", outputfile+".tbz2", outputfile +".tar"]
        subprocess.call(command)
        dest_format = "tbz2"
    else:
        command = ["7za", "a", outputfile + "." + dest_format.lower()] + files 
        subprocess.call(command)

    outputfile = outputfile + "." + dest_format.lower()
    
    object_name = os.path.join(os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
    if config['LOCAL']:
        return object_name

    s3 = boto3.client('s3')
    response = s3.upload_file(
        outputfile, 
        config['BUCKET'], 
        object_name
    )

    for file_object in file_objects:
        file_object = json.loads(file_object)
        shutil.rmtree(os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path'])))

    return [s3.generate_presigned_url('get_object', ExpiresIn=86400, Params={'Bucket': config['BUCKET'], 'Key': object_name})]
