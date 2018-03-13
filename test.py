from PIL import Image, ImageFont, ImageDraw

img = Image.open('./test.jpg')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("LiberationSans-Bold.ttf", 100)
text = "LGTM!"
shadowcolor = "yellow"
fillcolor = "red"

draw.text((0, 0), text,(255,255,255),font=font)

# https://mail.python.org/pipermail/image-sig/2009-May/005681.html
x, y = 10, 10
draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
draw.text((x+1, y+1), text, font=font, fill=shadowcolor)

draw.text((x-1, y), text, font=font, fill=shadowcolor)
draw.text((x+1, y), text, font=font, fill=shadowcolor)
draw.text((x, y-1), text, font=font, fill=shadowcolor)
draw.text((x, y+1), text, font=font, fill=shadowcolor)

draw.text((x, y), text, font=font, fill=fillcolor)


img.save('out.jpg')

