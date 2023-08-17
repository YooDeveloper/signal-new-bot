import random
from PIL import Image, ImageDraw, ImageFont

def addText(text_string):
  ran = random.randint(1111,9999)
  img = Image.open('dt/tem.jpg')
  img.save(f"dt/{ran}.jpg")
  img = Image.open(f"dt/{ran}.jpg")
  font = ImageFont.truetype("dt/JetBrainsMono-Bold.ttf", size=150)
  idraw = ImageDraw.Draw(img)
  idraw.text((50, 50), text_string, font=font)
  img.save(f"dt/{ran}.jpg")
  return f"dt/{ran}.jpg"

# img = Image.open('dt/bg.jpg')
# img = img.resize((640, 360))
# img.save(f"dt/tem.jpg")

# font1 = ImageFont.truetype("dt/JetBrainsMono-Bold.ttf", size=120)
# font2 = ImageFont.truetype("dt/FiraCodeRegular.ttf", size=100)
# font3 = ImageFont.truetype("dt/JetBrainsMono-Bold.ttf", size=90)
# idraw = ImageDraw.Draw(img)
# idraw.text((400, 150), "КУРС RUB/USD", font=font1, fill="#ecf0f1")
# idraw.text((150, 400), "ПОКУПКА", font=font2, fill="#f5f6fa")
# idraw.text((1130, 400), "ПРОДАЖА", font=font2, fill="#f5f6fa")
# idraw.text((220, 530), "66,4", font=font3)
# idraw.text((1250, 530), "76,4", font=font3, fill="#dcdde1")
# img.save(f"dt/template.jpg")