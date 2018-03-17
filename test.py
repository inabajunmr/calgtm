from PIL import Image, ImageFont, ImageDraw
import urllib.request
import io

def lgtm(img, fillcolor="white", shadowcolor="black"):
    ## TODO get size of image
    ## TODO adjust font size
    ## TODO adjust place of text
    font_size = 100;
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("LiberationSans-Bold.ttf", font_size)
    text = "LGTM!"

    # place of text
    x, y = 10, 10

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
    img = Image.open(img_binary)
    return img

img = get_img('https://pbs.twimg.com/media/DWZ0jPVV4AAFm7S.jpg:large')
## TODO compress image
lgtm(img)
