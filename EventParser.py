import pytesseract
from PIL import Image
from datetime import datetime
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import re
from dateutil.parser import parse
from ics import Calendar, Event
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

def extract_text(image_path):
    # Perform OCR using Tesseract
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
        with open('output.txt', 'w') as f:
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
    fields = find_fields(extract_text("SampleFlyers/11.png")) 
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
