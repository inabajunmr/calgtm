from PIL import Image, ImageFont, ImageDraw

img = Image.open('./test.jpg')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("LiberationSans-Bold.ttf", 42)
draw.text((0, 0),"LGTM!",(255,255,255),font=font)
img.save('out.jpg')

