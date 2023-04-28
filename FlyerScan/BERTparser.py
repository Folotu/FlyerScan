import re
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer, BartForConditionalGeneration

custom_cache_dir = "../HuggingFaceModels"

ner_model = pipeline(
    'ner',
    model=AutoModelForTokenClassification.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english', cache_dir=custom_cache_dir),
    tokenizer=AutoTokenizer.from_pretrained('dbmdz/bert-large-cased-finetuned-conll03-english', cache_dir=custom_cache_dir),
    aggregation_strategy="simple",
)

summarizer = pipeline(
    'summarization',
    model=BartForConditionalGeneration.from_pretrained('sshleifer/distilbart-cnn-12-6', cache_dir=custom_cache_dir),
    tokenizer=AutoTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6', cache_dir=custom_cache_dir)
)

def BertGens(text):

    titleSum = summarizer(text, max_length=8, min_length=1, do_sample=False)
    title = titleSum[0]['summary_text']

    entities = ner_model(text)

    date = None
    time = None
    start_time = None
    end_time = None
    location = None
    description = None

    # Extract start and end times
    time_pattern = re.compile(r'(\d{1,2}:\d{2}\s*[AP]M)\s*-\s*(\d{1,2}:\d{2}\s*[AP]M)')
    time_match = time_pattern.search(text)
    if time_match:
        start_time = time_match.group(1)
        end_time = time_match.group(2)

    # Set the description as a summary of the text
    summary = summarizer(text, max_length=35, min_length=10, do_sample=False)
    description = summary[0]['summary_text']

    # Use regex to extract the date
    date_pattern = re.compile(r'(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})')
    date_match = date_pattern.search(text)
    if date_match:
        date = date_match.group(1)
    else:
        for entity in entities:
            if entity['entity_group'] == 'DATE' and not date:
                date = entity['word']

    # Use regex to extract the location
    location_pattern = re.compile(r'(Location\s*:\s*)([^\n]+)')
    location_match = location_pattern.search(text)
    if location_match:
        location = location_match.group(2)
    else:
        for entity in entities:
            if entity['entity_group'] == 'LOC' and not location:
                location = entity['word']

    fields = {
        "title": title,
        "date": date,
        "time": None,
        "start_time": start_time,
        "end_time": end_time,
        "location": location,
        "desc": description
    }

    return fields

