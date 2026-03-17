import spacy
import re


nlp = spacy.load("en_core_web_sm")


def mask_sensitive_data(text: str) -> str:
    
    '''
    I am using regex and spacy to mask the sensitive info. They both provide good accuracy and and low latency.
    For better accuracy we can finetune too.
    '''
    
    #Mask emails and phones using regex
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, "[EMAIL_REDACTED]", text)

    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    text = re.sub(phone_pattern, "[PHONE_REDACTED]", text)

    #Mask Names, Organizations, and Locations using spaCy NER
    doc = nlp(text)
    
    for ent in reversed(doc.ents):
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            text = text[:ent.start_char] + f"[{ent.label_}_REDACTED]" + text[ent.end_char:]
            
    return text

