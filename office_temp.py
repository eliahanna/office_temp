import requests
import json
import datetime
import colorsys
import time
from sys import exit
import unicornhathd

try:
        from PIL import Image, ImageDraw, ImageFont
except ImportError:
        exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

# The lines that will be displayed on LED matrix
lines = []

def getWeather():
    weather_api = 'ca21216fd309c93287df5ad643170ed1'
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Seattle&appid="+weather_api+"&units=imperial")
    # parse response
    response_str = ""
    for line in response:
        response_str += line.decode("utf-8") 
        # parse json
    response_json = json.loads(response_str)
    current_temp = response_json["main"]["temp"]
    min_temp = response_json["main"]["temp_min"]
    max_temp = response_json["main"]["temp_max"]
    return str(current_temp), str(min_temp), str(max_temp)

def getCurrentDateTime():
    current_time = datetime.datetime.now()
    return current_time.strftime('%m/%d/%y %I:%M %p')

current_temp, min_temp, max_temp = getWeather()

weather_line = "Current temp: "+current_temp + " Min temp: " +  min_temp +  " Max temp: "  + max_temp
lines.append(weather_line)

current_time_line = getCurrentDateTime()
lines.append(current_time_line)

colours = [tuple([int(n * 255) for n in colorsys.hsv_to_rgb(x / float(len(lines)), 1.0, 1.0)]) for x in range(len(lines))]

# Use `fc-list` to show a list of installed fonts on your system,
# or `ls /usr/share/fonts/` and explore.

FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12)

# sudo apt install fonts-droid
# FONT = ('/usr/share/fonts/truetype/droid/DroidSans.ttf', 12)

# sudo apt install fonts-roboto
# FONT = ('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 10)

unicornhathd.rotation(270)
unicornhathd.brightness(0.6)

width, height = unicornhathd.get_shape()

text_x = width
text_y = 2


font_file, font_size = FONT

font = ImageFont.truetype(font_file, font_size)

text_width, text_height = width, 0

try:
    for line in lines:
        w, h = font.getsize(line)
        text_width += w + width
        text_height = max(text_height, h)
                                        
    text_width += width + text_x + 1
    image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    offset_left = 0

    for index, line in enumerate(lines):
        draw.text((text_x + offset_left, text_y), line, colours[index], font=font)
        offset_left += font.getsize(line)[0] + width

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x + scroll, y)) 
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(width - 1 - x, y, r, g, b)
        unicornhathd.show()
        time.sleep(0.01)

except KeyboardInterrupt:
        unicornhathd.off()

finally:
        unicornhathd.off()
