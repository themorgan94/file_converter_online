from flask_babel import gettext as _

available_filetypes = {
    "image": {
        "title": _("Image Converter"),
        "description": _("Here, you can find an image converter for your needs, for example, a PDF to image converter."),
        "long-description": _("A list with our free online image converter that convert to a variety of target formats. You can also apply effects or enhance images during conversion. Just select your format you want to convert to, upload your image file and optionally select filters. Your image will be converted instantly and you can download the result after only a couple of seconds."),
        "icon-class": "fa fa-file-image-o",
        "ext": ["BMP","EPS","GIF","ICO","JPG","PNG","SVG","TGA","TIFF","WBMP","WebP"],
        "allowed": ["BMP","EPS","GIF","ICO","JPG", "JPEG","PNG","SVG","TGA","TIFF","WBMP","WebP"],
        "options" : {
            "type": "object",
            "title": _("Options"),
            "properties": {
                "change_size": {
                    "type": "object",
                    "title": _("Change Size"),
                    "format": "grid",
                    "properties": {
                        "width": {
                            "type": "integer",
                            "minimum": 1
                        },
                        "height": {
                            "type": "integer",
                            "minimum": 1
                        }
                    }
                },
                "color": {
                    "type": "string",
                    "enum" : [
                        "Gray", "Monochrome", "Negate", "Year 1980", "Year 1900"
                    ]
                },
                "enhancement": {
                    "type": "array",
                    "uniqueItems": True,
                    "format": "checkbox",
                    "items": {
                        "type": "string",
                        "enum" : [
                            "Deskew","Equalize","Normalize","Enhance",
                            "Sharpen","No Antialias","Despeckle"
                        ]
                    }
                },
                "dpi": {
                    "type": "integer",
                    "minimum": 10,
                    "maximum": 1200
                },
                "cropFrom": {
                    "type": "object",
                    "title": _("Crop from"),
                    "format": "grid",
                    "properties": {
                        "top": {
                            "type": "integer"
                        },
                        "bottom": {
                            "type": "integer"
                        },
                        "left": {
                            "type": "integer"
                        },
                        "right": {
                            "type": "integer"
                        }
                    }
                },
                "blackAndWhiteTreshold": {
                    "type": "integer",
                    "title": _("Black and white threshold"),
                    "minimum": 1,
                    "maximum": 255
                }
            }
          }
    },
    "audio": {
        "title": _("Audio Converter"),
        "description": _("A versatile online audio converter to convert audio files in the most common audio"),
        "long-description" : "This is a list with the audio conversion tools we provide. We support the conversion from over 50 source formats. You can see the details on the converter page. Just select your target converter and start uploading your files. All audio converters can also rip the audio from a video file.",
        "icon-class": "fa fa-music",
        "ext": ["AAC","AIFF","FLAC","M4V","MMF","MP3","OGG","OPUS","WAV","WMA"],
        "allowed": ["AAC","AIFF","FLAC","M4V","MMF","MP3","OGG","OPUS","WAV","WMA", "3G2","3GP","AVI","FLV","MKV","MOV","MP4","MPG","OGV","WEBM","WMV"],
        "options" : {
            "type": "object",
            "title": _("Options"),
            "properties": {
                "bitrate": {
                    "title": _("Change audio bitrate"),
                    "type": "string",
                    "enum": ["6 kbps","8 kbps","12 kbps","16 kbps","24 kbps","32 kbps","48 kbps","56 kbps","64 kbps","96 kbps","112 kbps","128 kbps","160 kbps","192 kbps","224 kbps","256 kbps","320 kbps"]
                },
                "frequency": {
                    "title": _("Change sampling rate"),
                    "type": "string",
                    "enum": ["1000 Hz","8000 Hz","11025 Hz","16000 Hz","22050 Hz","24000 Hz","32000 Hz","44100 Hz","48000 Hz","96000 Hz"]
                },
                "channels": {
                    "title": _("Change audio channels"),
                    "type": "string",
                    "enum": ["mono","stereo"]
                },
                "trim": {
                    "title": _("Trim audio"),
                    "type": "object",
                    "properties": {
                        "audio_start": {
                            "title": _("From"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        },
                        "audio_end": {
                            "title": _("To"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "video": {
        "title": _("Video Converter"),
        "description": _("Convert video files into the most common formats, such as MP4, AVI, MOV, and more"),
        "long-description": _("This is a list with our free online video converter we have so far. Please choose the link you wish to convert your video file to."),
        "icon-class": "fa fa-film",
        "ext": ["3G2","3GP","AVI","FLV","MKV","MOV","MP4","MPG","OGV","WEBM","WMV"],
        "allowed": ["3G2","3GP","AVI","FLV","MKV","MOV","MP4","MPG","OGV","WEBM","WMV"],
        "options" : {
            "type": "object",
            "title": _("Options"),
            "properties": {
                "bitrate": {
                    "title": _("Change audio bitrate"),
                    "type": "integer",
                    "description": _("in kbps")
                },
                "framerate": {
                    "title": _("Change frame rate"),
                    "type": "integer",
                    "description": _("per second")
                },
                "trim": {
                    "title": _("Trim video"),
                    "type": "object",
                    "properties": {
                        "video_start": {
                            "title": _("From"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        },
                        "video_end": {
                            "title": _("To"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        }
                    }
                },
                "rotate": {
                    "title": _("Rotate video (clockwise)"),
                    "type": "string",
                    "enum": ["90", "180", "270"]
                },
                "flip": {
                    "title": _("Mirror/flip video"),
                    "type": "string",
                    "enum": ["Horizontally", "Vertically"]
                }
                
            }
        }
    },
    "document": {
        "title": _("Document Converter"),
        "description": _("Our free document converter selection that allows you to convert Word to PDF, JPG to PDF any many more."),
        "long-description": _("This is a list with the free online document converter we offer."),
        "icon-class": "fa fa-file",
        "ext": ["DOC","DOCX","HTML","ODT","PDF","PPT","PPTX","RTF","TXT","XLSX"],
        "allowed": ["DOC","DOCX","HTML","ODT","PDF","PPT","PPTX","RTF","TXT","XLSX"],
        "disallowed" : {
            "PPT": [ "TXT" ],
            "PPTX": [ "TXT" ],
            "XLSX": [ "TXT" ]
        },
        "options" : {
        }
    },
    "archive": {
        "title": _("Archive Converter"),
        "description": _("Create archive files like a ZIP with this free compression tool."),
        "long-description": _("This is our list of the online archive converter we provide. You can either compress your file to a specific archive format or convert one archive to another format."),
        "icon-class": "fa fa-file-archive-o",
        "ext": ["7Z","TAR.BZ2","TAR.GZ","ZIP"],
        "allowed" : [],
        "options" : {
        }
    },
    "ebook": {
        "title": _("Ebook Converter"),
        "description": _("A list of versatile online ebook converter that can convert your text documents to ebook easily."),
        "long-description": _("Our online ebook converter support a variety of input formats like PDF, ePub, HTML, LIT, LRF, mobi and more. Choose the target format you need for your ebook reader below and start converting."),
        "icon-class": "fa fa-book",
        "ext": ["AZW3","EPUB","FB2","LIT","LRF","MOBI","PDB","PDF","TCR"],
        "allowed": ["AZW3","EPUB","FB2","LIT","LRF","MOBI","PDB","PDF","TCR"],
        "options" : {
            "type": "object",
            "title": _("Options"),
            "properties": {
                "target": {
                    "title": _("Target ebook reader"),
                    "type": "string",
                    "enum": ["cybookg3","cybook_opus","default","generic_eink","generic_eink_hd","generic_eink_large","hanlinv3","hanlinv5","illiad","ipad","ipad3","irexdr1000","irexdr800","jetbook5","kindle","kindle_dx","kindle_fire","kindle_oasis","kindle_pw","kindle_pw3","kindle_voyage","kobo","msreader","mobipocket","nook","nook_color","nook_hd_plus","pocketbook_900","pocketbook_pro_912","galaxy","sony","sony300","sony900","sony-landscape","sonyt3","tablet"]
                },
                "title": {
                    "title": _("Change ebook title"),
                    "type": "string"
                },
                "author": {
                    "title": _("Change ebook author"),
                    "type": "string"
                },
                "font": {
                    "title": _("Set base font size (in pts)"),
                    "type": "integer",
                    "options": {
                        "inputAttributes": {
                          "placeholder": "6 - 22"
                        }
                    }
                },
                "encoding": {
                    "title": _("Change input encoding"),
                    "type": "string",
                    "enum": ["UTF8","ISO8859_1 (Latin Alphabet No. 1)","Cp1252 (WindowsLatin-1)","ISO8859_2 (Latin Alphabet No. 2)","ISO8859_4(Latin Alphabet No. 4)","ISO8859_5 (Latin/Cyrillic Alphabet)","ISO8859_7 (Latin/Greek Alphabet)","ISO8859_9 (Latin Alphabet No. 9)","ISO8859_13 (Latin Alphabet No. 13)","ISO8859_15 (Latin Alphabet No. 15)","ASCII","Cp1250(Windows  Eastern European)","Cp1251(Windows  Cyrillic)","Cp1253(Windows  Greek)","Cp1254(Windows  Turkish)","Cp1257(Windows  Baltic)","KOI8_R (Russian)","UTF-16","EUC_JP (Japanese)","SJIS (Shift-JIS, Japanese)","ISO2022JP (ISO 2022, Japanese)","GB2312 (Simplified Chinese)","GBK (Simplified Chinese)","ISCII91 (encoding of Indic scripts)","Big5 (Traditional Chinese)","TIS620 (Thai)","ISO-2022-KR (Korean)"],
                    "description": _("For expert only")
                },
                "ascii": {
                    "title": _("ASCII output"),
                    "type": "boolean",
                    "format": "checkbox",
                    "description": _("For expert only")
                },
                "heuristics": {
                    "title": _("Enable heuristics"),
                    "type": "boolean",
                    "format": "checkbox",
                    "description": _("For expert only")
                }
            }
        }
    },
    "device": {
        "title": _("Device Converter"),
        "type": "Video",
        "description": _("A collection of online video converter for your mobile device, gaming console or tablet."),
        "long-description": _("This is a list of devices we support with optimized conversion settings. You can convert a file optimized for hardware like a smartphone, a gaming console, a TV or to burn a proper data volume. Our converter knows the screen size of your devices and can optimize quality and file size for it. Just select the converter for your device below."),
        "icon-class": "fa fa-tablet",
        "ext": ["Android","Blackberry","iPad","iPhone","iPod","PlayStation","PSP","Wii","XBOX"],
        "allowed": ["3G2","3GP","AVI","FLV","MKV","MOV","MP4","MPG","OGV","WEBM","WMV"],
        "options" : {
            "type": "object",
            "title": _("Options"),
            "properties": {
                "size": {
                    "title": _("Set video size"),
                    "type": "string",
                    "description": _("Video size property works only on android, ipad and iphone devices."),
                    "enum": ["480x270", "480x360", "640x360", "1280x720", "1920x1080"]
                },
                "disableAudio": {
                    "title": _("Disable audio track"),
                    "type": "boolean",
                    "format": "checkbox"
                },
                "trim": {
                    "title": _("Cut video"),
                    "type": "object",
                    "properties": {
                        "video_start": {
                            "title": _("From"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        },
                        "video_end": {
                            "title": _("To"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "webservice": {
        "title": _("Webservice Converter"),
        "type": "Video",
        "description": _("Convert and optimize your files for webservices like WhatsApp, Twitter, Facebook, and many more."),
        "long-description": _("This free online file converter lets you convert your files so they can easily be upload to webservices like Youtube, Instagram and the like. It's possible to upload a file that is not recognized by these webservices and convert it using presets to a format that is supported by these websites."),
        "icon-class": "fa fa-globe",
        "ext": ["Dailymotion","Facebook","Instagram","Telegram","Twitch","Twitter","Viber","Vimeo","WhatsApp","Youtube"],
        "allowed": ["3G2","3GP","AVI","FLV","MKV","MOV","MP4","MPG","OGV","WEBM","WMV"],
        "options" : {
            "type": "object",
            "title": _("Options"),
            "properties": {
                "size": {
                    "title": _("Set video size"),
                    "type": "string",
                    "enumSource": [{
                        "source" : [
                            "DailymotionHQ 1280x720 (HD) 25fps","DailymotionHQ 1280x720 (HD) 30fps","DailymotionHQ 1920x1080 (Full HD) 25fps","DailymotionHQ 1920x1080 (Full HD) 30fps","DailymotionHQ 480p 25fps","DailymotionHQ 480p 30fps","DailymotionMQ 1280x720 (HD) 25fps","DailymotionMQ 1280x720 (HD) 30fps","DailymotionMQ 1920x1080 (Full HD) 25fps","DailymotionMQ 1920x1080 (Full HD) 30fps","DailymotionMQ 480p 25fps","DailymotionMQ 480p 30fps",
                            "Facebook- keep dimensions","FacebookHQ 1280x720 (HD) 23.976fps","FacebookHQ 1280x720 (HD) 25fps","FacebookHQ 1280x720 (HD) 30fps","FacebookHQ 1920x1080 (Full HD) 23.976fps","FacebookHQ 1920x1080 (Full HD) 25fps","FacebookHQ 1920x1080 (Full HD) 30fps","FacebookHQ 2k 23.976fps","FacebookHQ 2k 25fps","FacebookHQ 2k 30fps","FacebookHQ 360p 23.976fps","FacebookHQ 360p 25fps","FacebookHQ 360p 30fps","FacebookHQ 480p 23.976fps","FacebookHQ 480p 25fps","FacebookHQ 480p 30fps","FacebookHQ 4K (UHD) 23.976fps","FacebookHQ 4K (UHD) 25fps","FacebookHQ 4K (UHD) 30fps","FacebookMQ 1280x720 (HD) 23.976fps","FacebookMQ 1280x720 (HD) 25fps","FacebookMQ 1280x720 (HD) 30fps","FacebookMQ 1920x1080 (Full HD) 23.976fps","FacebookMQ 1920x1080 (Full HD) 25fps","FacebookMQ 1920x1080 (Full HD) 30fps","FacebookMQ 2k 23.976fps","FacebookMQ 2k 25fps","FacebookMQ 2k 30fps","FacebookMQ 360p 23.976fps","FacebookMQ 360p 25fps","FacebookMQ 360p 30fps","FacebookMQ 480p 25fps","FacebookMQ 480p 30fps","FacebookMQ 480p 33.976fps","FacebookMQ 4K (UHD) 23.976fps","FacebookMQ 4K (UHD) 25fps","FacebookMQ 4K (UHD) 30fps",
                            "Instagram 1280x720 (HD)","Instagram 1920x1080 (Full HD)","Instagram 640x360",
                            "Telegram 1280x720 (HD)","Telegram 1920x1080 (Full HD)","Telegram 640x360","Telegram 854x480",
                            "Twitch HQ 1280x720 (Full HD) 25fps","Twitch HQ 1280x720 (Full HD) 30fps","Twitch HQ 1280x720 (Full HD) 50fps","Twitch HQ 1280x720 (Full HD) 60fps","Twitch HQ 1920x1080 (Full HD) 25fps","Twitch HQ 1920x1080 (Full HD) 30fps","Twitch HQ 1920x1080 (Full HD) 50fps","Twitch HQ 1920x1080 (Full HD) 60fps","Twitch HQ 360p 25fps","Twitch HQ 360p 30fps","Twitch HQ 360p 50fps","Twitch HQ 360p 60fps","Twitch HQ 480p 25fps","Twitch HQ 480p 30fps","Twitch HQ 480p 50fps","Twitch HQ 480p 60fps","Twitch MQ 1280x720 (Full HD) 25fps","Twitch MQ 1280x720 (Full HD) 30fps","Twitch MQ 1280x720 (Full HD) 50fps","Twitch MQ 1280x720 (Full HD) 60fps","Twitch MQ 1920x1080 (Full HD) 25fps","Twitch MQ 1920x1080 (Full HD) 30fps","Twitch MQ 1920x1080 (Full HD) 50fps","Twitch MQ 1920x1080 (Full HD) 60fps","Twitch MQ 360p 25fps","Twitch MQ 360p 30fps","Twitch MQ 360p 50fps","Twitch MQ 360p 60fps","Twitch MQ 480p 25fps","Twitch MQ 480p 30fps","Twitch MQ 480p 50fps","Twitch MQ 480p 60fps",
                            "Twitter 1280x720 (HD) 25fps","Twitter 1280x720 (HD) 30fps","Twitter 320x180 25fps","Twitter 320x180 30fps","Twitter 640x360 25fps","Twitter 640x360 30fps",
                            "Viber 1280x720 (HD)","Viber 1920x1080 (Full HD)","Viber 640x360","Viber 854x480",
                            "Vimeo - keep dimensions","Vimeo HQ 1280x720 (HD) 23.976fps","Vimeo HQ 1280x720 (HD) 25fps","Vimeo HQ 1280x720 (HD) 30fps","Vimeo HQ 1280x720 (HD) 50fps","Vimeo HQ 1280x720 (HD) 60fps","Vimeo HQ 1920x1080 (Full HD) 23.976fps","Vimeo HQ 1920x1080 (Full HD) 25fps","Vimeo HQ 1920x1080 (Full HD) 30fps","Vimeo HQ 1920x1080 (Full HD) 50fps","Vimeo HQ 1920x1080 (Full HD) 60fps","Vimeo HQ 2k 23.976fps","Vimeo HQ 2k 25fps","Vimeo HQ 2k 30fps","Vimeo HQ 2k 50fps","Vimeo HQ 2k 60fps","Vimeo HQ 360p 23.976fps","Vimeo HQ 360p 25fps","Vimeo HQ 360p 30fps","Vimeo HQ 360p 50fps","Vimeo HQ 360p 60fps","Vimeo HQ 480p 23.976fps","Vimeo HQ 480p 25fps","Vimeo HQ 480p 30fps","Vimeo HQ 480p 50fps","Vimeo HQ 480p 60fps","Vimeo HQ 4K (UHD) 23.976fps","Vimeo HQ 4K (UHD) 25fps","Vimeo HQ 4K (UHD) 30fps","Vimeo HQ 4K (UHD) 50fps","Vimeo HQ 4K (UHD) 60fps","Vimeo MQ 1280x720 (HD) 23.976fps","Vimeo MQ 1280x720 (HD) 25fps","Vimeo MQ 1280x720 (HD) 30fps","Vimeo MQ 1280x720 (HD) 50fps","Vimeo MQ 1280x720 (HD) 60fps","Vimeo MQ 1920x1080 (Full HD) 23.976fps","Vimeo MQ 1920x1080 (Full HD) 25fps","Vimeo MQ 1920x1080 (Full HD) 30fps","Vimeo MQ 1920x1080 (Full HD) 50fps","Vimeo MQ 1920x1080 (Full HD) 60fps","Vimeo MQ 2k 23.976fps","Vimeo MQ 2k 25fps","Vimeo MQ 2k 30fps","Vimeo MQ 2k 50fps","Vimeo MQ 2k 60fps","Vimeo MQ 360p 23.976fps","Vimeo MQ 360p 25fps","Vimeo MQ 360p 30fps","Vimeo MQ 360p 50fps","Vimeo MQ 360p 60fps","Vimeo MQ 480p 23.976fps","Vimeo MQ 480p 25fps","Vimeo MQ 480p 30fps","Vimeo MQ 480p 50fps","Vimeo MQ 480p 60fps","Vimeo MQ 4K (UHD) 23.976fps","Vimeo MQ 4K (UHD) 25fps","Vimeo MQ 4K (UHD) 50fps","Vimeo MQ 4K (UHD) 60fps","Vimeo MQ 4K (UHD), 30fps",
                            "WhatsApp 1024x576","WhatsApp 1280x720 (HD)","WhatsApp 480x270","WhatsApp 640x360",
                            "Youtube - keep dimensions","Youtube HQ 1280x720 (HD) 23.976fps","Youtube HQ 1280x720 (HD) 25fps","Youtube HQ 1280x720 (HD) 30fps","Youtube HQ 1280x720 (HD) 50fps","Youtube HQ 1280x720 (HD) 60fps","Youtube HQ 1920x1080 (Full HD) 23.976fps","Youtube HQ 1920x1080 (Full HD) 25fps","Youtube HQ 1920x1080 (Full HD) 30fps","Youtube HQ 1920x1080 (Full HD) 50fps","Youtube HQ 1920x1080 (Full HD) 60fps","Youtube HQ 2k 23.976fps","Youtube HQ 2k 25fps","Youtube HQ 2k 30fps","Youtube HQ 2k 50fps","Youtube HQ 2k 60fps","Youtube HQ 360p 23.976fps","Youtube HQ 360p 30fps","Youtube HQ 360p 50fps","Youtube HQ 360p 60fps","Youtube HQ 360p, 25fps","Youtube HQ 480p 23.976fps","Youtube HQ 480p 25fps","Youtube HQ 480p 30fps","Youtube HQ 480p 50fps","Youtube HQ 480p 60fps","Youtube HQ 4K (UHD) 23.976fps","Youtube HQ 4K (UHD) 25fps","Youtube HQ 4K (UHD) 30fps","Youtube HQ 4K (UHD) 50fps","Youtube HQ 4K (UHD) 60fps","Youtube MQ 1280x720 (HD) 23.976fps","Youtube MQ 1280x720 (HD) 25fps","Youtube MQ 1280x720 (HD) 30fps","Youtube MQ 1280x720 (HD) 50fps","Youtube MQ 1280x720 (HD) 60fps","Youtube MQ 1920x1080 (Full HD) 23.976fps","Youtube MQ 1920x1080 (Full HD) 25fps","Youtube MQ 1920x1080 (Full HD) 30fps","Youtube MQ 1920x1080 (Full HD) 50fps","Youtube MQ 1920x1080 (Full HD) 60fps","Youtube MQ 2k 23.976fps","Youtube MQ 2k 25fps","Youtube MQ 2k 30fps","Youtube MQ 2k 50fps","Youtube MQ 2k 60fps","Youtube MQ 360p 23.976fps","Youtube MQ 360p 25fps","Youtube MQ 360p 30fps","Youtube MQ 360p 50fps","Youtube MQ 360p 60fps","Youtube MQ 480p 23.976fps","Youtube MQ 480p 25fps","Youtube MQ 480p 30fps","Youtube MQ 480p 50fps","Youtube MQ 480p 60fps","Youtube MQ 4K (UHD) 23.976fps","Youtube MQ 4K (UHD) 25fps","Youtube MQ 4K (UHD) 30fps","Youtube MQ 4K (UHD) 50fps","Youtube MQ 4K (UHD) 60fps"
                        ],
                        "filter": "webserviceFilterCB",
                        "title": "{{item}}",
                        "value": "{{item}}"
                    }]
                },
                "disableAudio": {
                    "title": _("Disable audio track"),
                    "type": "boolean",
                    "format": "checkbox"
                },
                "trim": {
                    "title": _("Cut video"),
                    "type": "object",
                    "properties": {
                        "video_start": {
                            "title": _("From"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        },
                        "video_end": {
                            "title": _("To"),
                            "type": "string",
                            "options": {
                                "inputAttributes": {
                                  "placeholder": "00:00:00"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "pdf": {
        "title": _("PDF Converter"),
        "type": "PDF",
        "_prefix": _("Convert {}"),
        "description": _("This PDF converter allows you to convert PDF to images and others available format."),
        "long-description": _("This PDF converter allows you to convert PDF to images and others available format."),
        "icon-class": "fa fa-file-pdf-o",
        "ext": ["PDF-to-Images", "Images-to-PDF"],
        "allowed": ["PDF","PNG", "JPG", "JPEG", "BMP"],
        "disallowed" : {
            "PDF-to-Images": ["PNG", "JPG", "JPEG", "BMP"],
            "Images-to-PDF": ["PDF"]
        },
        "options" : {
        }
    },
    "document-compressor": {
        "category": "tool",
        "title": _("Compress Documents"),
        "type" : _("Compress document files"),
        "_prefix": "Compress {}",
        "description": _("Reduce the file size of larger PDF documents"),
        "long-description": _("With this free online document compression tool, you can reduce the file size of larger PDF documents. Use this document compressor to optimize your documents for uploading them or for sending them via e-mail or messenger. Make documents smaller - online and for free."),
        "icon-class": "fa fa-file-o ",
        "ext": ["PDF_dc"],
        "allowed": ["PDF"],
        "options" : {
        }
    },
    "image-compressor": {
        "category": "tool",
        "title": _("Compress Images"),
        "type" : _("Compress image files"),
        "_prefix": _("Compress {}"),
        "description": _("Reduce the file size of your pictures, photos, graphics, and more with versatile image compression."),
        "long-description": _("Make all kinds of image files smaller when it comes to size. All you need is this free online image compressor. Reduce the file size of your pictures, photos, graphics, and more with versatile image compression. "),
        "icon-class": "fa fa-picture-o",
        "ext": ["JPG_ic", "PNG_ic", "SVG_ic"],
        "allowed": ["JPG", "JPEG", "PNG", "SVG"],
        "disallowed" : {
            "PNG": [ "JPG", "JPEG" ],
            "JPEG": [ "PNG" ],
            "JPG": [ "PNG" ],
            "SVG": [ "PNG", "JPG", "JPEG" ]
        },
        "options" : {
        }
    },
    "video-compressor": {
        "category": "tool",
        "title": _("Compress Videos"),
        "type" : _("Compress video files"),
        "_prefix": _("Compress {}"),
        "description": _("Reduce the video file size using our free, online video compressor."),
        "long-description": _("You can easily reduce the video file size using our free, online video compressor. Send videos via WhatsApp, messengers, or e-mail or upload them to YouTube and other video platforms. Video compression makes sure that your videos are not too big."),
        "icon-class": "fa  fa-file-video-o",
        "ext": ["MP4_vc"],
        "allowed": ["MP4"],
        "options" : {
        }
    }
}