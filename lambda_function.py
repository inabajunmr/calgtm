import requests
from PIL import Image, ImageFont, ImageDraw
import urllib.request
import io
import base64

def lambda_handler(event, context):
    img_url = event["queryStringParameters"]['img']

    try:
        img_binary = get_img(assemble_query_parameter(event["queryStringParameters"], img_url))
        lgtm_img_binary = lgtm(img_binary)
        return generate_response(200, {"Content-Type": "image/jpeg"}, True, base64.b64encode(lgtm_img_binary).decode('utf-8'))
    except BaseException as err:
        # when occur error, return default error lgtm image.
        img_binary = io.BytesIO(open("error_image.jpg", "rb").read())
        img = Image.open(img_binary)
        output = io.BytesIO()
        img.save(output, format='JPEG')
        return generate_response(200, {"Content-Type": "image/jpeg"}, True, base64.b64encode(output.getvalue()).decode('utf-8'))

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

def lgtm(img_binary, fillcolor="white", shadowcolor="black"):
    img = Image.open(img_binary)

    # convert to jpg
    img.convert("RGB")
    # compress for too big image
    img.thumbnail((1024, 1024), Image.ANTIALIAS)
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
    draw.text((x, y-1), text, font=font, fill=shadowcolor)
    draw.text((x, y+1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y), text, font=font, fill=shadowcolor)
    draw.text((x+1, y+1), text, font=font, fill=shadowcolor)
    draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
    draw.text((x-1, y), text, font=font, fill=shadowcolor)
    draw.text((x-1, y-1), text, font=font, fill=shadowcolor)

    # draw main text
    draw.text((x, y), text, font=font, fill=fillcolor)

    output = io.BytesIO()
    img.save(output, format='JPEG')
    return output.getvalue()

def get_img(url):
    req = urllib.request.Request(url)
    image_read = urllib.request.urlopen(req, timeout=3).read()
    img_binary = io.BytesIO(image_read)
    return img_binary

# # for test
# context = {}
# event = {
#     "queryStringParameters" : {
#         "img" : "https://example.com",
#         "key1" : "value1",
#         "key2" : "value2"
#     }
# }

# response = lambda_handler(event, context)
# # print(response["body"])