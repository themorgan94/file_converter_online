(function($) {
    jQuery.fn.drop_uploader = function(options) {
        options = $.extend({
            // Localization
            uploader_text: 'Drop files to upload, or',
            browse_text: 'Browse',
            only_one_error_text: 'Only one file allowed',
            not_allowed_error_text: 'File type is not allowed',
            big_file_before_error_text: 'Files, bigger than',
            big_file_after_error_text: 'is not allowed',
            allowed_before_error_text: 'Only',
            allowed_after_error_text: 'files allowed',
            // CSS
            browse_css_class: 'button button-primary',
            browse_css_selector: 'file_browse',
            uploader_icon: '<i class="pe-7s-cloud-upload"></i>',
            file_icon: '<i class="pe-7s-file"></i>',
            progress_color: '#4a90e2',
            // Main Options
            time_show_errors: 5,
            layout: 'thumbnails', // thumbnails/list
            method: 'normal', // normal/ajax/chunked
            chunk_size: 1000000, 
            // AJAX URL
            url: 'ajax_upload.php',
            delete_url: 'ajax_delete.php',
            btn_selector : ''
        }, options);

        this.each(function(i, val) {
            var v = val;
            // Get input file params
            var file_accept = $(v).attr("accept");
            var file_multiple = $(v).prop("multiple");
            var file_multiple_count = parseInt($(v).data("count"));
            var input_name = $(v).prop("name");
            var max_file_size = 0; 

            var uploader_id = 'drop_uploader_' + i;

            var added_files = 0;
            var files_index = 0;

            var cur_form = $(v).parent("form");
            var input_max_file_size = $(cur_form).find("input[name=MAX_FILE_SIZE]").val();
            if(input_max_file_size !== undefined) {
                max_file_size = parseInt(input_max_file_size);
            }

            var data_max_file_size = $(v).data("maxfilesize");
            if(data_max_file_size !== undefined) {
                max_file_size = parseInt(data_max_file_size);
            }

            var layout = options.layout;
            if($(v).data("layout") == "thumbnails") {
                layout = "thumbnails";
            } else if($(v).data("layout") == "list") {
                layout = "list";
            }

            var submit_method = options.method;
            if($(v).data("method") == "normal") {
                submit_method = "normal";
            } else if($(v).data("method") == "ajax") {
                submit_method = "ajax";
            } else if($(v).data("method") == "chunked") {
                submit_method = "chunked";
            }

            var submit_url = options.url;
            if($(v).data("url") != "" && $(v).data("url") !== undefined) {
                submit_url = $(v).data("url");
            }

            var delete_url = options.delete_url;
            if($(v).data("deleteurl") != "" && $(v).data("deleteurl") !== undefined) {
                delete_url = $(v).data("deleteurl");
            }

            // Wrap file input field
            $(v).attr('id', get_random_id());
            $(v).wrap('<div id="' + uploader_id + '" class="drop_uploader drop_zone"></div>');
            $(v).before('<div class="text_wrapper">' + options.uploader_icon + ' <span class="text">' + options.uploader_text + ' <a href="#" class="' + options.browse_css_class + ' ' + options.browse_css_selector + '">' + options.browse_text + '</a></span></div>');
            $(v).before('<span class="errors"></span>');
            if(submit_method == "ajax" || submit_method == "chunked") {
                $(v).attr('name', '');
            }

            var ul_classes = "files";

            if(layout == "thumbnails") {
                ul_classes += " thumb"
            }
            if(submit_method == "ajax") {
                ul_classes += " ajax"
            }
            if(submit_method == "chunked") {
                ul_classes += " ajax"
            }

            $(v).before('<ul class="' + ul_classes + '"></ul>');

            var drop_zone = $('#' + uploader_id);

            drop_zone[0].ondragover = function(event) {
                drop_zone.addClass('hover');
                if(submit_method == "normal") {
                    maximizeInput(v);
                    return false;
                } else if(submit_method == "ajax" || submit_method == "chunked"){
                    minimizeInput(v);
                    return false;
                }
                
            };

            drop_zone[0].ondragleave = function(event) {
                drop_zone.removeClass('hover');
                //minimizeInput(v);
                return false;
            };

            drop_zone[0].ondrop = function(event) {
                minimizeInput(v);
                clear_error();
                if(submit_method == "normal") {
                    var files = event.dataTransfer.files;
                    // Check Files
                    var check_result = check_files(files);
                    if(check_result == false) {
                        $('#' + uploader_id + ' .files').html('');
                        // Delete input and create new
                        var new_id = get_random_id();
                        var cur_input_html = $(v)[0].outerHTML;
                        var new_v = $.parseHTML(cur_input_html);
                        $(new_v).attr('id', new_id);
                        $(v).before(new_v);
                        $(v).remove();
                        v = $('#'+new_id)[0];
                        $(v).change(function() {
                            files_added();
                        });
                        event.preventDefault ? event.preventDefault() : (event.returnValue = false);
                    }
                } else if(submit_method == "ajax" || submit_method == "chunked") {
                    event.preventDefault ? event.preventDefault() : (event.returnValue = false);
                    var files = event.dataTransfer.files;
                    var check_result = check_files(files);
                    if(check_result) {
                        files_added(files);
                    }
                }
            };

            $(drop_zone).find("." + options.browse_css_selector).click(function(event) {
                event.preventDefault ? event.preventDefault() : (event.returnValue = false);
                $(v).click();
            });

            // Show added files
            $(v).change(function() {
                var files = $(v)[0].files;
                var check_result = check_files(files);

                if(submit_method == "normal") {
                    if(check_result == false) {
                        $('#' + uploader_id + ' .files').html('');
                        // Delete input and create new
                        var new_id = get_random_id();
                        var cur_input_html = $(v)[0].outerHTML;
                        var new_v = $.parseHTML(cur_input_html);
                        $(new_v).attr('id', new_id);
                        $(v).before(new_v);
                        $(v).remove();
                        v = $('#'+new_id)[0];
                        $(v).change(function() {
                            files_added();
                        });
                        event.preventDefault ? event.preventDefault() : (event.returnValue = false);
                    } else {
                        files_added(files);
                    }
                } else if(submit_method == "ajax" || submit_method == "chunked") {
                    if(check_result) {
                        files_added(files);
                    }
                }
            });

            function files_added(files) {
                if(files === undefined) {
                    var files = $(v)[0].files;
                }
                if(submit_method == "normal") {
                    $('#' + uploader_id + ' .files').html('');
                }
                for (var i = 0; i < files.length; i++) {
                    if(layout == "thumbnails") {
                        // Add file to list
                        $('#' + uploader_id + ' .files.thumb').append('<li id="selected_file_' + files_index + '"><div class="thumbnail"></div><span class="title" title="' + files[i].name + '"> ' + files[i].name + ' </span></li>');
                        // Thumbnail
                        preview_file(files[i],files_index);
                    } else {
                        // Add file to list
                        $('#' + uploader_id + ' .files').append('<li id="selected_file_' + files_index + '">' + options.file_icon + ' <span>' + files[i].name + '</span> </li>');
                    }
                    // Now upload files via AJAX
                    if(submit_method == "ajax") {
                        file_upload_ajax(files[i],files_index);
                    } else if(submit_method == "chunked") {
                        file_upload_chunked(files[i],files_index);
                    }
                    files_index++;
                    if(submit_method == "ajax" || submit_method == "chunked") {
                        added_files++;
                    }
                }
            }

            function preview_file(file, i) {
                var reader  = new FileReader();

                getOrientation(file, function(orientation) {
                    var rotate_class = "";
                    if(orientation == 8) {
                        rotate_class = "rotate_90";
                    } else if(orientation == 3) {
                        rotate_class = "rotate_180";
                    } else if(orientation == 6) {
                        rotate_class = "rotate_270";
                    }
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').addClass(rotate_class);
                });
                
                // Check file type
                if(file.type.match('image/*')) {
                    reader.readAsDataURL(file);
                } else if(file.type.match('video/*')) {
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').html('<i class="pe-7s-video"></i>');
                } else if(file.type.match('audio/*')) {
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').html('<i class="pe-7s-volume"></i>');
                } else {
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').html('<i class="pe-7s-file"></i>');
                }

                reader.onloadend = function () {
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').attr('style', 'background-image: url("' + reader.result + '")');
                    // Add hover layer
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').append('<div class="du_hover_layer"></div>');
                }
            }

            function file_upload_ajax(file,i) {
                $('#' + uploader_id).trigger( "file_upload_start", [ file.name ] );
                var xhr = new XMLHttpRequest();
                if(layout == "thumbnails") {
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').after('<div class="du_progress"></div>');
                } else {
                    $('#' + uploader_id + ' #selected_file_' + i).append('<div class="du_progress"></div>');
                }
                var progress_el = $('#' + uploader_id + ' #selected_file_' + i + ' .du_progress');
                (xhr.upload || xhr).addEventListener('progress', function(e) {
                    var done = e.position || e.loaded
                    var total = e.totalSize || e.total;
                    var progress = Math.round(done/total*100);
                    draw_round_progress(progress_el[0], progress / 100, layout);
                });
                $(options['btn_selector']).prop("disabled", true);
                xhr.addEventListener('load', function(e) {
                    var response = JSON.parse(this.response);
                    $('#' + uploader_id + ' #selected_file_' + i + ' .du_progress').fadeOut('slow');
                    if(response.success) {
                        $(options['btn_selector']).prop("disabled", false);
                        $('#' + uploader_id).trigger( "file_upload_end", [ file.name ] );
                        //
                        response.files.forEach(function(file_){
                            $("#converter-form").append(
                                `<input type='hidden' name='url[]' value='${JSON.stringify(file_)}'/>`
                            );
                            
                            // Add delete button
                            var du_delete_button = $('<i class="fa fa-trash action-delete" data-fileid="' + file_.path + '"></i>').hide();
                            if(layout == "thumbnails") {
                                $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').append(du_delete_button);
                            } else if (layout == "list") {
                                $('#' + uploader_id + ' #selected_file_' + i).append(du_delete_button);
                            }
                            du_delete_button.delay(500).fadeIn("slow");
                            // Add hidden input with file id
                            $('#' + uploader_id).append('<input id="hidden_file_' + i + '" type="hidden" name="' + input_name + '" value="' + response.file_id + '" >');
                            // Add delete buton listener
                            $('#' + uploader_id + ' #selected_file_' + i + ' i.action-delete').on("click", function(event) {
                                var fileid = $(this).data("fileid");
                                $.ajax({
                                    url: delete_url,
                                    data: "fileid=" + fileid,
                                }).done(function() {
                                    $('#' + uploader_id + ' #selected_file_' + i).delay(500).fadeOut("slow");
                                    $('#' + uploader_id + ' #hidden_file_' + i).remove();
                                    $("[value='"+JSON.stringify(file_)+"']").remove()
                                    added_files--;

                                    if($('[name="url[]"]').length <= 0){
                                        $(options['btn_selector']).prop("disabled", true);
                                    }
                                });
                            });
                        });
                    } else {
                        set_error(response.message);
                        remove_file(i);
                    }
                });
                xhr.open('post', submit_url, true);
                var fdata = new FormData;
                fdata.append(input_name.replace('[]',''), file);
                xhr.send(fdata);
            }

            function file_upload_chunked(file,i) {
                $('#' + uploader_id).trigger( "file_upload_start", [ file.name ] );

                if(layout == "thumbnails") {
                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').after('<div class="du_progress"></div>');
                } else {
                    $('#' + uploader_id + ' #selected_file_' + i).append('<div class="du_progress"></div>');
                }

                var size = file.size;
                var sliceSize = options.chunk_size;
                var start = 0;
                var chunk = 0;

                loop();

                function loop() {
                    var end = start + sliceSize;

                    if (size - end < 0) {
                        end = size;
                    }

                    var s = slice(file, start, end);

                    send(s, start, end, size, sliceSize);

                    chunk++;

                    if (end < size) {
                        start += sliceSize;
                    }
                }

                function send(piece, start, end, size, sliceSize) {
                    var formdata = new FormData();
                    var xhr = new XMLHttpRequest();

                    xhr.open('POST', submit_url, true);

                    formdata.append('start', start);
                    formdata.append('end', end);
                    formdata.append(input_name.replace('[]',''), piece);
                    formdata.append('chunk', chunk);
                    formdata.append('file_name', file.name);
                    if (end < size) {
                        formdata.append('chunk_last', false);
                    } else {
                        formdata.append('chunk_last', true);
                    }

                    xhr.onreadystatechange = function() {
                        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {

                            var response = JSON.parse(this.response);

                            // Draw progress
                            var progress_el = $('#' + uploader_id + ' #selected_file_' + i + ' .du_progress');

                            draw_round_progress(progress_el[0], end / size, layout);

                            if (end < size) {
                                loop();
                            } else if(response.success && response.type == 'file') {
                                // Upload Completed
                                $('#' + uploader_id + ' #selected_file_' + i + ' .du_progress').fadeOut('slow');

                                $('#' + uploader_id).trigger( "file_upload_end", [ file.name ] );
                                // Add delete button
                                var du_delete_button = $('<i class="fa fa-trash action-delete" data-fileid="' + response.file_id + '"></i>').hide();
                                if(layout == "thumbnails") {
                                    $('#' + uploader_id + ' #selected_file_' + i + ' div.thumbnail').append(du_delete_button);
                                } else if (layout == "list") {
                                    $('#' + uploader_id + ' #selected_file_' + i).append(du_delete_button);
                                }
                                du_delete_button.delay(500).fadeIn("slow");
                                // Add hidden input with file id
                                $('#' + uploader_id).append('<input id="hidden_file_' + i + '" type="hidden" name="' + input_name + '" value="' + response.file_id + '" >');
                                // Add delete buton listener
                                $('#' + uploader_id + ' #selected_file_' + i + ' i.action-delete').on("click", function(event) {
                                    var fileid = $(this).data("fileid");
                                    $.ajax({
                                        url: delete_url,
                                        data: "fileid=" + fileid,
                                    }).done(function() {
                                        $('#' + uploader_id + ' #selected_file_' + i).delay(500).fadeOut("slow");
                                        $('#' + uploader_id + ' #hidden_file_' + i).remove();
                                        added_files--;
                                    });
                                });
                            }
                        }
                    }

                    xhr.send(formdata);
                }
            }

            function slice(file, start, end) {
                var slice = file.mozSlice ? file.mozSlice :
                            file.webkitSlice ? file.webkitSlice :
                            file.slice ? file.slice : noop;

                return slice.bind(file)(start, end);
            }

            function noop() {
  
            }

            function remove_file(i) {
                $('#' + uploader_id + ' #selected_file_' + i).delay(options.time_show_errors * 1000).fadeOut("slow");
            }

            function set_error(text) {
                $('#' + uploader_id + ' .errors').html('<p>' + text + '</p>');
                if (options.time_show_errors > 0) {
                    setTimeout(clear_error, options.time_show_errors * 1000);
                }
            }

            function clear_error() {
                $('#' + uploader_id + ' .errors p').fadeOut("slow", function() {
                    $('#' + uploader_id + ' .errors p').remove();
                });
            }

            function get_file_size_readable(bytes) {
                if      (bytes>=1000000000) {bytes=(bytes/1000000000).toFixed(2)+' GB';}
                else if (bytes>=1000000)    {bytes=(bytes/1000000).toFixed(2)+' MB';}
                else if (bytes>=1000)       {bytes=(bytes/1000).toFixed(2)+' KB';}
                else if (bytes>1)           {bytes=bytes+' bytes';}
                else if (bytes==1)          {bytes=bytes+' byte';}
                else                        {bytes='0 byte';}
                return bytes;
            };

            function check_files(files) {
                var allow_file_add = true;
                // Check multiple file support
                if (file_multiple) {
                    if(file_multiple_count) {
                        console.log(added_files);
                        if ((files.length + added_files) > file_multiple_count) {
                            set_error(options.allowed_before_error_text + ' ' + file_multiple_count + ' ' + options.allowed_after_error_text);
                            if(submit_method == "normal") {
                                added_files = 0;
                            }
                            return false;
                        } else {
                            allow_file_add = true;
                        }
                    } else {
                        allow_file_add = true;
                    }
                } else {
                    if (files.length > 1 || added_files > 0) {
                        set_error(options.only_one_error_text);
                        return false;
                    } else {
                        allow_file_add = true;
                    }
                }
                // Check file type support
                if(file_accept === undefined) {
                    allow_file_add = true;
                } else {
                    var accept_array = file_accept.split(',');
                    for (var i = 0; i < files.length; i++) {
                        var match_count = 0;
                        for (var a = 0; a < accept_array.length; a++) {
                            var match_string = accept_array[a].replace('/','.').trim();
                            if(match_string == "")
                                continue;
                            //if(files[i].type.match(match_string) != null) {
                            if( "." + files[i].name.split('.').pop().trim().toLowerCase() == match_string.toLowerCase() ){
                                //console.log(match_string, files[i].type);
                                match_count++;
                            }
                        }
                        if(match_count == 0) {
                            set_error(options.not_allowed_error_text);
                            return false;
                        }
                    }
                }
                // Check file size
                for (var i = 0; i < files.length; i++) {
                    if(files[i].size > max_file_size && max_file_size > 0) {
                        set_error(options.big_file_before_error_text + ' ' + get_file_size_readable(max_file_size) + ' ' + options.big_file_after_error_text);
                        return false;
                    }
                }
                return allow_file_add;
            }

            function maximizeInput(v) {
                var drop_zone = $(v).parent(".drop_zone");
                var position = drop_zone.position();
                var top = position.top + parseInt(drop_zone.css('marginTop'), 10);
                var left = position.left + parseInt(drop_zone.css('marginLeft'), 10);
                $(v).css({top: top, left: left, position:'absolute', width: drop_zone.width(), height: drop_zone.height(), display:'block'});
            }

            function minimizeInput(v) {
                $(v).css({display:'none'});
            }

            function get_random_id() {
                var text = "";
                var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

                for( var i=0; i < 15; i++ )
                    text += possible.charAt(Math.floor(Math.random() * possible.length));

                return text;
            }

            function draw_round_progress(el, percent, layout) {

                var canvas = el.children[0];

                var color = hex_to_rgba(options.progress_color);

                if(canvas === undefined) {
                    canvas = document.createElement('canvas');    
                }

                if(layout == "thumbnails") {
                    canvas.width = 100;
                    canvas.height = 100;
                    canvas.style.width = "50px";
                    canvas.style.height = "50px";
                    var diameter = 96;
                    var line_width = 8;
                } else {
                    canvas.width = 48;
                    canvas.height = 48;
                    canvas.style.width = "24px";
                    canvas.style.height = "24px";
                    var diameter = 48;
                    var line_width = 4;
                }

                el.appendChild(canvas);
                    
                if (typeof(G_vmlCanvasManager) !== 'undefined') {
                    G_vmlCanvasManager.initElement(canvas);
                }

                var ctx = canvas.getContext('2d');

                ctx.translate(diameter / 2, diameter / 2); // change center
                ctx.rotate((-1 / 2 + 0 / 180) * Math.PI); // rotate -90 deg
                
                var radius = (diameter - line_width) / 2; 
                percent = Math.min(Math.max(0, percent || 1), 1);
                ctx.beginPath();
                ctx.arc(0, 0, radius, 0, Math.PI * 2 * percent, false);
                ctx.strokeStyle = color;
                ctx.lineCap = 'round'; // butt, round or square
                ctx.lineWidth = line_width;
                ctx.stroke();
            }

            function hex_to_rgba(hex) {
                var c;
                if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
                    c= hex.substring(1).split('');
                    if(c.length== 3){
                        c= [c[0], c[0], c[1], c[1], c[2], c[2]];
                    }
                    c= '0x'+c.join('');
                    return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+',.8)';
                } else {
                    // return default color
                    return 'rgba(74, 144, 226, .8)';
                }
            }

            function getOrientation(file, callback) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var view = new DataView(e.target.result);
                    if (view.getUint16(0, false) != 0xFFD8) return callback(-2);
                    var length = view.byteLength, offset = 2;
                    while (offset < length) {
                        var marker = view.getUint16(offset, false);
                        offset += 2;
                        if (marker == 0xFFE1) {
                            if (view.getUint32(offset += 2, false) != 0x45786966) return callback(-1);
                            var little = view.getUint16(offset += 6, false) == 0x4949;
                            offset += view.getUint32(offset + 4, little);
                            var tags = view.getUint16(offset, little);
                            offset += 2;
                            for (var i = 0; i < tags; i++)
                            if (view.getUint16(offset + (i * 12), little) == 0x0112)
                                return callback(view.getUint16(offset + (i * 12) + 8, little));
                        }
                        else if ((marker & 0xFF00) != 0xFF00) break;
                        else offset += view.getUint16(offset, false);
                    }
                    return callback(-1);
                };
                reader.readAsArrayBuffer(file);
            }
        });
    };
})(jQuery);