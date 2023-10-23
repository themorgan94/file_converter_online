from wand.image import Image
from wand.color import Color
import os
import uuid
from flask import json
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
    with Image(filename = os.path.join(config['UPLOAD_DIR'], file_object['path'])) as img:
        if "change_size" in options:
            if 'width' in options['change_size'] \
                and 'height' in options['change_size']:
                if dest_format.lower() == "ico" and options['change_size']['width'] > 256 and options['change_size']['width'] > 256 :
                    options['change_size']['height'] = 256
                    options['changes_size']['width'] = 256

                img.resize(options['change_size']['width'], options['change_size']['height'])
            elif 'width' in options['change_size']:
                
                if dest_format.lower() == "ico" and options['change_size']['width'] > 256 :
                    options['change_size']['height'] = 256
                    options['change_size']['width'] = 256
                    img.resize(options['change_size']['width'], options['change_size']['height'])
                elif dest_format.lower() == "ico" and options['change_size']['width'] <= 256:
                    options['change_size']['height'] = options['change_size']['width']
                    img.resize(options['change_size']['width'], options['change_size']['height'])
                else:
                    img.transform(
                        resize = "{}".format(options['change_size']['width'])
                    )
            elif 'height' in options['change_size']:
                if dest_format.lower() == "ico" and options['change_size']['height'] > 256 :
                    options['change_size']['width'] = 256
                    options['change_size']['height'] = 256
                    img.resize(options['change_size']['width'], options['change_size']['height'])
                elif dest_format.lower() == "ico" and options['change_size']['height'] <= 256:
                    options['change_size']['width'] = options['change_size']['height']
                    img.resize(options['change_size']['width'], options['change_size']['height'])
                else:
                    img.transform(
                        resize = "x{}".format(options['change_size']['height'])
                    )

        if dest_format.lower() == "ico":
            if "width" not in options['change_size'] and "height" not in  options['change_size'] :
                img.resize(256, 256)

        if 'color' in options:
            color = options['color']
            if color == "Gray":
                img.transform_colorspace('gray')
            elif color == "Monochrome":
                img.transform_colorspace('gray')
                img.threshold()
            elif color == "Negate":
                img.negate()
            elif color == "Year 1980":
                img.sepia_tone(0.75)
            elif color == "Year 1900":
                img.transform_colorspace('gray')
                img.modulate(120,10,100),
                img.font_color = Color("#222b6d")
                img.gamma(0.5)
                img.contrast()
                img.brightness_contrast(30)

        if 'enhancement' in options and len(options['enhancement']) > 0:
            enhancements = options['enhancement']
            for enhancement in enhancements:
                if enhancement == 'Equalize':
                    img.equalize()
                elif enhancement == 'Normalize':
                    img.normalize()
                elif enhancement == 'Enhance':
                    img.enhance()
                elif enhancement == 'Sharpen':
                    img.sharpen()
                elif enhancement == 'No Antialias':
                    img.antialias = False
                elif enhancement == 'Despeckle':
                    img.despeckle()
                elif enhancement == 'Deskew':
                    img.deskew(0.8)

        if 'dpi' in options:
            dpi = int(options['dpi'])
            img.resolution = (dpi, dpi)
            img.units = 'pixelsperinch'

        if 'cropFrom' in options:
            if 'top' in options['cropFrom'] and \
                'bottom' in options['cropFrom'] and \
                'left' in options['cropFrom'] and \
                'right' in options['cropFrom']:
                img.crop(options['cropFrom']['left'],
                        options['cropFrom']['top'],
                        options['cropFrom']['right'],
                        options['cropFrom']['bottom'])
        
        if 'blackAndWhiteTreshold' in options:
            img.threshold(options['blackAndWhiteTreshold']/255)

        outputfile = os.path.join(config['UPLOAD_DIR'], os.path.dirname(file_object['path']), file_object['name'] + "." + dest_format.lower())
        with img.convert(dest_format) as converted:
            converted.save(filename=outputfile)
        
        
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