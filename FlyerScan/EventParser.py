import pytesseract
from PIL import Image
from datetime import datetime
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import re
from dateutil.parser import parse
from icalendar import Calendar, Event
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os
from io import BytesIO
import shutil
import arrow
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

    # img = Image.open(filepath)
    # img = img.resize((434,600), Image.Resampling.LANCZOS)
    # image_file_name_without_extension = os.path.splitext(filepath)[0]
    # output_file_name = image_file_name_without_extension + "_Resized.png"
    response = requests.get(filepath)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        resized_img = img.resize((434,600), Image.Resampling.LANCZOS)
        output = BytesIO()
        resized_img.save(output, format="PNG")
        output.seek(0)
        return output
    else:
        raise Exception(f"Failed to fetch image: {response.status_code}")

    # print('resized')
    # img.save(output_file_name, optimize=True, quality=85)
    # return output_file_name

    # url = f'https://resize.sardo.work/?imageUrl={image_url}&width={1000}&height={1000}'
    # response = requests.get(url, stream=True)
    # print(response.raw)

    # with open('sample.png', 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)

    # print('The file was saved successfully')

def sizeIsOK(filepath):
    # img = Image.open(filepath)
    # # get width and height
    # width = img.width
    # height = img.height
    # if (width > 1000 or height > 1000):
    #     return False
    # elif (os.stat(filepath)).st_size >= 1000000:
    #     return False
    # else:
    #     return True
    
    response = requests.get(filepath)

    if response.status_code == 200:
        # Get the size of the file in bytes from the Content-Length header
        file_size = int(response.headers.get('Content-Length', 0))
        img = Image.open(BytesIO(response.content))
        width, height = img.size

        if file_size >= 1000000:
                return False
        elif (width > 1000 or height > 1000):
            return False
        else:
            return True
    else:
        raise Exception(f"Failed to fetch image: {response.status_code}")


# def ocr_space_file(filename, overlay=False, language='eng'):

#     #overlay = True
#     payload = {'isOverlayRequired': overlay,
#                'apikey': os.getenv('OCR_API_KEY'),
#                'language': language,
#                'OCREngine': 5
#                }
#     with open(filename, 'rb') as f:
#         r = requests.post('https://api.ocr.space/parse/image',
#                           files={filename: f},
#                           data=payload,
#                           )
#     print(r.status_code)
#     print(r.reason)
#     rDict = json.loads(r.content.decode())

#     if overlay:
#         createOverlay(image_file_name=filename, json_file_data=rDict)

#     # Extract the ParsedText value from the dictionary
#     prsdText = ""
#     if "ParsedResults" in rDict and len(rDict["ParsedResults"]) > 0 and "ParsedText" in rDict["ParsedResults"][0]:
#         prsdText = rDict["ParsedResults"][0]["ParsedText"]

#     return prsdText

def ocr_space_url(url, fileData, overlay=False, language='eng'):
    #overlay = True
    if url is not None:
        payload = {'url': url,
                'isOverlayRequired': overlay,
                'apikey': os.getenv('OCR_API_KEY'),
                'language': language}
        r = requests.post('https://api.ocr.space/parse/image', data=payload)

    else:
        payload = {'isOverlayRequired': overlay,
                'apikey': os.getenv('OCR_API_KEY'),
                'language': language,
                'OCREngine': 5 }

        files = {
        "file": ("resized_image.jpg", fileData, "image/png"),}
        r = requests.post('https://api.ocr.space/parse/image', 
                      data=payload, files=files)

    print(r.status_code)
    print(r.reason)
    rDict = json.loads(r.content.decode())

    # if overlay:
    #     createOverlay(image_file_name=filename, json_file_data=rDict)

    # Extract the ParsedText value from the dictionary
    prsdText = ""
    if "ParsedResults" in rDict and len(rDict["ParsedResults"]) > 0 and "ParsedText" in rDict["ParsedResults"][0]:
        prsdText = rDict["ParsedResults"][0]["ParsedText"]

    return prsdText


def extract_text(image_path):
    # Perform OCR using Tesseract
    # with Image.open(image_path) as img:
    #     text = pytesseract.image_to_string(img)
    #     with open('output.txt', 'w') as f:
    #         f.write(text)

    # check image dimensions
    if not sizeIsOK(image_path):
        imageData = imageResize(image_path)
        # Perform OCR using API
        text = ocr_space_url(url=None, fileData=imageData)
        with open('outputWithAPI.txt', 'w', encoding="utf-8") as f:
            f.write(text)
    else:
        # Perform OCR using API
        # text = ocr_space_file(filename=image_path)
        text = ocr_space_url(url=image_path, fileData=None)
        with open('outputWithAPI.txt', 'w', encoding="utf-8") as f:
            f.write(text)

    return text

def find_fields(text):
    # Define patterns for extracting information
    title_pattern = r"\b(?:[A-Z][a-z]*\s){1,4}(?:[A-Z][a-z]*)\b"
    date_pattern = r"(?i)(?:(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:\s+\d{4})?"
    time_pattern = r"\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)"
    time_range_pattern = r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM))\s*-\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM))\b"
    # location_pattern = r"(?i)\b(?:at|in)\b\s+(?:the\s+)?(.+)"
    location_pattern = r"(?i)(?:in\s+|at\s+|on\s+)?(?:the\s+)?(?:[A-Z][a-z]+\s+)*?(?:Building|Hall|Center|Campus|Office|Room|Suite|Theater)(?:\s+[A-Z][a-z]+)*(?:\s*,\s*|\s+in\s+|\s+at\s+|\s+on\s+)?(?:[A-Za-z]+\s+)*?\d+(?:-\d+)?(?:\s+[A-Za-z]+\b(?:\s+[A-Za-z]+)*)?"

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
                if chunk.label() == 'LOC':
                    loc.append(' '.join([c[0] for c in chunk]))
                elif chunk.label() == 'ORGANIZATION':
                    org.append(' '.join([c[0] for c in chunk]))
    
    # Extract location from the text
    if location_match:
        loc.append(' '.join(location_match.group().splitlines()))
    
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

def convert_time_to_24h(time_str):
    time_str = time_str.lower()
    match = re.match(r"(\d?\d)[:\s]?(\d\d)?\s*([ap]m?)", time_str)
    if not match:
        raise ValueError("Invalid time format")

    hours = int(match.group(1))
    minutes = int(match.group(2)) if match.group(2) else 0
    am_pm = match.group(3)
    if "p" in am_pm and hours != 12:
        hours += 12
    elif "a" in am_pm and hours == 12:
        hours = 0

    return hours, minutes

def calendarGen(fields):
    title = fields['title']
    date = fields['date']
    if fields['start_time'] or fields['end_time']:
        startTimeHrs, startTimeMins = convert_time_to_24h(fields['start_time'])
        endTimeHrs, endTimeMins = convert_time_to_24h(fields['end_time'])
    else: 
        time = fields['time']
        if time is not None:
            startTimeHrs, startTimeMins = convert_time_to_24h(time)
            endTimeHrs, endTimeMins = 0, 0
        else: 
            startTimeHrs, startTimeMins, endTimeHrs, endTimeMins = 0, 0, 0, 0
    location = fields['location']
    desc= fields['desc']

    c = Calendar()

    c.add('prodid', '-//FlyerScan Calendar//mxm.dk//')
    c.add('version', '2.0')
    e = Event()
    e.add('summary', str(title))

    if date is None: 
        date = '1999-09-09'

    dt = datetime.strptime(date, '%Y-%m-%d')

    e.add('dtstart', datetime(dt.year, dt.month, dt.day, startTimeHrs, startTimeMins, 0, tzinfo=None))
    e.add('dtend', datetime(dt.year, dt.month, dt.day, endTimeHrs, endTimeMins, 0, tzinfo=None))


    e.add('dtstamp', arrow.get().datetime)
    e.add('priority', 5)

    e['organizer'] = ' '.join(fields['org'])
    e['location'] = str(location)
    e['description'] = str(desc)
    c.add_component(e)


    with open('SampleIcsGens/my.ics', 'wb') as my_file:
        my_file.write(c.to_ical())
    
    return str(title), date, fields['time'],fields['start_time'], fields['end_time'], desc, location


def startEventParsing(imageURLorPath):
    try:
        fields = find_fields(extract_text(imageURLorPath)) 
        title, date, time, startime, endtime, desc, location = calendarGen(fields=fields)

        if not startime or date:
            from .BERTparser import BertGens
            f = open("outputWithApi.txt", "r")
            print("Used BERT1")
            bertFields = BertGens(f.read())
            if bertFields['date'] is None and date is not None:
                bertFields['date'] = date
            if bertFields['start_time'] is None and startime is not None:
                bertFields['start_time'] = startime
            return bertFields
        
        return fields

    except AttributeError as e:
        print("Error:", e)
        try: 
            from .BERTparser import BertGens
            f = open("outputWithApi.txt", "r")
            print("Used BERT")
            return BertGens(f.read())
            
        except:
            title, date, time, desc = None, None, None, ""
            return {}


        # print("Title:", title)
        # print("Date:", date)
        # print("Time:", time)
        # print("start time:", startime)
        # print("end time:", endtime)
        # print("Location:", location)
        # print("Description:", desc)

