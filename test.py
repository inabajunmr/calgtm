from PIL import Image, ImageFont, ImageDraw
import urllib.request
import io

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

    font = ImageFont.truetype("LiberationSans-Bold.ttf", int(font_size))
    text = "LGTM!"

    # TODO adjust place of text(https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil)
    x, y = 40, 40

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

    img.save('out.jpg')

def get_img(url):
    req = urllib.request.Request(url)
    image_read = urllib.request.urlopen(req).read()
    img_binary = io.BytesIO(image_read)
    return img_binary

img_binary = get_img('https://pbs.twimg.com/media/DWZ0jPVV4AAFm7S.jpg:large')
lgtm(img_binary)
