import requests
from PIL import Image, ImageFont, ImageDraw
import urllib.request
import io
import base64
import logging
import time
import re
from logging import getLogger, StreamHandler, Formatter

# log setting
logger = getLogger("Logger")
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

def lambda_handler(event, context):
    img_url = event["queryStringParameters"]['img']
    if(re.match("^https?://.*" , img_url) == None):
        img_url = "http://" + img_url

    try: 
        try:
            logger.debug("Start get image")
            img_binary = get_img(assemble_query_parameter(event["queryStringParameters"], img_url))

            logger.debug("End get image")
        except BaseException as err:
            if(re.match("^https?://.*" , img_url) == None):
                img_url = "https://" + img_url
                logger.debug("Start get image")
                img_binary = get_img(assemble_query_parameter(event["queryStringParameters"], img_url))
                logger.debug("End get image")

        img = Image.open(img_binary)
        format = img.format

        output = io.BytesIO()
        if format == "GIF":
            lgtm_gif = process_gif(img_binary)        

            if len(lgtm_gif) == 1:
                lgtm_gif[0].save(output, optimize=True, format=format)
            else:
                lgtm_gif[0].save(output, optimize=True, save_all=True, append_images=lgtm_gif[1:], loop=1000, format=format)
        else:            
            logger.debug("Start open image")
            img = Image.open(img_binary)
            logger.debug("end open image")
            logger.debug("Start lgtm image")
            lgtm_image = lgtm(img)
            logger.debug("end lgtm image")
            logger.debug("Start save image")
            lgtm_image.save(output, optimize=True, format=format)
            logger.debug("End lgtm image")

        return generate_response(200, {"Content-Type": generate_content_type(format)}, True, base64.b64encode(output.getvalue()).decode('utf-8'))
        
    except BaseException as err:
        logger.debug("Error")
        logger.debug(err)

        img_binary = io.BytesIO(open("error_image.jpg", "rb").read())
        img = Image.open(img_binary)
        output = io.BytesIO()
        img.save(output, format='JPEG')
        return generate_response(200, {"Content-Type": "image/jpeg"}, True, base64.b64encode(output.getvalue()).decode('utf-8'))


def generate_content_type (format):
    return "image/" + format.lower()
    
def generate_response(status_code, headers, is_base_64_encoded, body):
    response = {
       "statusCode": status_code,
       "headers": headers,
       "isBase64Encoded": is_base_64_encoded,
        "body" : body
    }
    return response

# when img parameter's url has multiple query parameters, this can not be interpreted part of url.
# so must assemble img to original image url
def assemble_query_parameter(query_parameters, url):
    for k, v in query_parameters.items():
        if k != "img":
            url = url + "&" + k + "=" + v

    return url

def lgtm(img, fillcolor="white", shadowcolor="black"):
    width, height = img.size

    # adjust font size
    font_size = width / 2 if width <= height else height / 2

    draw = ImageDraw.Draw(img)

    # calculate text size
    font_name = "LiberationSans-Bold.ttf"
    font = ImageFont.truetype(font_name, int(font_size))
    text = "LGTM!"
    text_w, text_h = draw.textsize(text, font)

    # resize font size until text does not run off image.
    while text_w > width or text_h > height:
        font_size = font_size - 1
        font = ImageFont.truetype(font_name, int(font_size))
        text_w, text_h = draw.textsize(text, font)

    # adjust place of text
    x, y = (width - text_w)/2, (height - text_h)/2

    # draw border
    border_bold = width/200
    if border_bold < 3:
        border_bold = 3

    draw.text((x,             y-border_bold), text, font=font, fill=shadowcolor)
    draw.text((x,             y+border_bold), text, font=font, fill=shadowcolor)
    draw.text((x+border_bold, y-border_bold), text, font=font, fill=shadowcolor)
    draw.text((x+border_bold, y), text, font=font, fill=shadowcolor)
    draw.text((x+border_bold, y+border_bold), text, font=font, fill=shadowcolor)
    draw.text((x-border_bold, y+border_bold), text, font=font, fill=shadowcolor)
    draw.text((x-border_bold, y), text, font=font, fill=shadowcolor)
    draw.text((x-border_bold, y-border_bold), text, font=font, fill=shadowcolor)

    # draw main text
    draw.text((x, y), text, font=font, fill=fillcolor)

    # discarding the alpha channel. JPEGs can't represent an alpha channel.
    if img.mode in ('RGBA', 'LA'):
        background = Image.new(img.mode[:-1], img.size, "white")
        background.paste(img, img.split()[-1])
        img = background

    return img

def get_img(url):
    req = urllib.request.Request(url)
    image_read = urllib.request.urlopen(req, timeout=3).read()
    img_binary = io.BytesIO(image_read)
    return img_binary

# reference:https://stackoverflow.com/questions/41718892/pillow-resizing-a-gif
def get_gif_mode(img_binary):
    img = Image.open(img_binary)
    try:
        while True:
            if img.tile:
                if img.tile[0][1][2:] != img.size:
                    return "partial"
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    return "full"

def process_gif(img_binary):
    img = Image.open(img_binary)
    mode = get_gif_mode(img_binary)

    p = img.getpalette()
    last_frame = img.convert('RGBA')
    all_frames = []
    i = 0
    try:
        while True:
            if not img.getpalette():
                img.putpalette(p)

            new_frame = Image.new('RGBA', img.size)

            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(img, (0, 0), img.convert('RGBA'))

            new_frame = lgtm(new_frame)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    return all_frames

# for test
# context = {}
# event = {
#     "queryStringParameters" : {
#         "img" : "http://example.com/image.jpg",
#         "key1" : "value1",
#         "key2" : "value2"
#     }
# }

# response = lambda_handler(event, context)
# print(response["body"])
