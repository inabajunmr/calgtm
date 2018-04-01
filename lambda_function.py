import requests
from PIL import Image, ImageFont, ImageDraw
import urllib.request
import io
import base64

def lambda_handler(event, context):
    img_url = event["queryStringParameters"]['img']
    # TODO handling exception
    img_binary = get_img(img_url)
    lgtm_img_binary = lgtm(img_binary)
    response = {
       "statusCode": 200,
       "headers":{
           "Content-Type": "image/jpeg",
       },
       "isBase64Encoded": True,
        "body" : base64.b64encode(lgtm_img_binary).decode('utf-8')
       }
    return response

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
    image_read = urllib.request.urlopen(req).read()
    img_binary = io.BytesIO(image_read)
    return img_binary

# for test
# context = {}
# event = {
#     "queryStringParameters" : {
#         "img" : "https://example.jpg"
#     }
# }

# response = lambda_handler(event, context)
# print(response["body"])