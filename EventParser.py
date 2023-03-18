import pytesseract
from PIL import Image
from datetime import datetime
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import re
from dateutil.parser import parse
from ics import Calendar, Event
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os
import shutil
from dotenv import load_dotenv
load_dotenv()

# try: 
#     nltk.data.find('tokenizers/punkt')
#     nltk.data.find('averaged_perceptron_tagger')
#     nltk.data.find('tokenizers/maxent_ne_chunker')
#     nltk.data.find('tokenizers/words')
# except LookupError: 
#     nltk.download('punkt')
#     nltk.download('averaged_perceptron_tagger')
#     nltk.download('maxent_ne_chunker')
#     nltk.download('words')

def createOverlay(image_file_name, json_file_data):
    unicode_font_name = "Fonts/BOD_R.ttf"
    TINT_COLOR = (255, 255, 0) 
    TRANSPARENCY = .70  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    img = Image.open(image_file_name)
    img = img.convert("RGBA")

    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.

    #file_name_with_extension = os.path.basename(image_file_name)  # Extracts the file name with the extension
    image_file_name_without_extension = os.path.splitext(image_file_name)[0]  # Removes the extension from the file name

    for pr in json_file_data["ParsedResults"]:
        for line in pr["TextOverlay"]["Lines"]:
            for w in line["Words"]:
                x1 = (w["Left"], w["Top"])
                x2 = (x1[0] + w["Width"], x1[1] + w["Height"])

                # Adjust font size according to the rectangle height
                font_size = abs(x1[1] - x2[1])
                font = ImageFont.truetype(unicode_font_name, int(font_size))
                draw.rectangle((x1, x2), fill=TINT_COLOR+(OPACITY,))

                text = w["WordText"]

                draw.text(x1, text, fill=(255, 0, 0, 255), font=font)
  
    img = Image.alpha_composite(img, overlay)

    output_file_name = image_file_name_without_extension + "_overlay.png"
    img.save(output_file_name)
    img.show()

def imageResize(filepath):

    # basewidth = 1000
    img = Image.open(filepath)
    # wpercent = (basewidth/float(img.size[0]))
    # hsize = int((float(img.size[1])*float(wpercent)))
    # print(hsize)
    # hsize = 1000
    img = img.resize((1000,1000), Image.Resampling.LANCZOS)
    image_file_name_without_extension = os.path.splitext(filepath)[0]
    output_file_name = image_file_name_without_extension + "_Resized.png"

    print('resized')
    img.save(output_file_name)
    return output_file_name

    # url = f'https://resize.sardo.work/?imageUrl={image_url}&width={1000}&height={1000}'
    # response = requests.get(url, stream=True)
    # print(response.raw)

    # with open('sample.png', 'wb') as out_file:
    # shutil.copyfileobj(response.raw, out_file)

    # print('The file was saved successfully')

def sizeIsOK(filepath):
    img = Image.open(filepath)
    
    # get width and height
    width = img.width
    height = img.height

    if (width > 1000 or height > 1000):
        return False
    else:
        return True

def ocr_space_file(filename, overlay=False, language='eng'):

    #overlay = True
    payload = {'isOverlayRequired': overlay,
               'apikey': os.getenv('OCR_API_KEY'),
               'language': language,
               'OCREngine': 5
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    rDict = json.loads(r.content.decode())

    if overlay:
        createOverlay(image_file_name=filename, json_file_data=rDict)

    # Extract the ParsedText value from the dictionary
    prsdText = ""
    if "ParsedResults" in rDict and len(rDict["ParsedResults"]) > 0 and "ParsedText" in rDict["ParsedResults"][0]:
        prsdText = rDict["ParsedResults"][0]["ParsedText"]

    return prsdText


def extract_text(image_path):
    # Perform OCR using Tesseract
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
        with open('output.txt', 'w') as f:
            f.write(text)

    # check image dimensions
    if not sizeIsOK(image_path):
        image_path = imageResize(image_path)
        
    # Perform OCR using API
    text = ocr_space_file(filename=image_path)
    with open('outputWithAPI.txt', 'w') as f:
            f.write(text)

    
    return text

def find_fields(text):
    # Define patterns for extracting information
    title_pattern = r"\b(?:[A-Z][a-z]*\s){1,4}(?:[A-Z][a-z]*)\b"
    date_pattern = r"(?i)(?:(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:\s+\d{4})?"
    time_pattern = r"\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)"
    time_range_pattern = r"\b(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM))\s*-\s*(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM))\b"
    location_pattern = r"(?i)\b(?:at|in)\b\s+(?:the\s+)?(.+)"

    # Extract information from the text using regex
    title_match = re.search(title_pattern, text)
    date_match = re.search(date_pattern, text)
    time_range_match = re.search(time_range_pattern, text)
    time_match = re.search(time_pattern, text) if not time_range_match else None
    location_match = re.search(location_pattern, text)
    title = ' '.join(title_match.group().split()[:5]) if title_match else None
    date = parse(date_match.group()).strftime("%Y-%m-%d") if date_match else None
    start_time = time_range_match.group(1) if time_range_match else None
    end_time = time_range_match.group(2) if time_range_match else None
    time = start_time if start_time else (time_match.group() if time_match else None)
    desc = ""

    # Use NER to extract location and organization
    loc = []
    org = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if isinstance(chunk, Tree):
                if chunk.label() == 'GPE':
                    loc.append(' '.join([c[0] for c in chunk]))
                elif chunk.label() == 'ORGANIZATION':
                    org.append(' '.join([c[0] for c in chunk]))
    
    # Extract location from the text
    if location_match:
        loc.append(location_match.group(1))
    
    # Build the description based on the extracted information
    if date:
        if start_time and end_time:
            desc += f"The event takes place on {date} from {start_time} to {end_time}."
        elif time:
            desc += f"The event takes place on {date} at {time}."
        else:
            desc += f"The event takes place on {date}."
    if loc:
        desc += f" The event location is {', '.join(loc)}."
    if org:
        desc += f" The event is organized by {', '.join(org)}."
    fields = {
        'title': title,
        'date': date,
        'time': time,
        'start_time': start_time,
        'end_time': end_time,
        'location': loc,
        'desc': desc,
        'org': org
    }
    return fields


try:
    fields = find_fields(extract_text("SampleFlyers/2.png")) 
    title = fields['title']
    date = fields['date']
    if fields['start_time'] or fields['end_time']:
        time = str(fields['start_time']) + str(fields['end_time'])
    else: 
        time = fields['time']
    # start_time = fields['start_time']
    # end_time = fields['end_time']
    location = fields['location']
    desc= fields['desc']

    c = Calendar()
    e = Event()
    e.name = str(title)
    e.begin = date
    # e.end: ArrowLike = None,
    # e.duration: timedelta = None,
    e.location = str(location)
    e.description = str(desc)
    e.organizer = ' '.join(fields['org'])
    c.events.add(e)
    print(c.events)

    with open('SampleIcsGens/my.ics', 'w') as my_file:
        my_file.writelines(c.serialize_iter())

except AttributeError as e:
    print("Error:", e)
    title, date, time, desc = None, None, None, ""


print("Title:", title)
print("Date:", date)
print("Time:", time)
print("Location:", location)
print("Description:", desc)

