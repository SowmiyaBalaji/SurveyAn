from googletrans import Translator
from langdetect import detect


def detect_indian_language(text):
    try:
        lang_code = detect(text)
        if lang_code == 'en':
            lan = 'English'
        elif lang_code == 'hi':
            lan = 'Hindi'
        elif lang_code == 'ta':
            lan = 'Tamil'
        elif lang_code == 'te':
            lan = 'Telugu'
        elif lang_code == 'kn':
            lan = 'Kannada'
        elif lang_code == 'ml':
            lan = 'Malayalam'
        elif lang_code == 'bn':
            lan = 'Bengali'
        elif lang_code == 'mr':
            lan = 'Marathi'
        # Add more Indian languages as needed with their respective language codes.
        else:
            lan = 'Unknown'
    except:
        lan = 'Unknown'
    return [lang_code, lan]


def translate_to_english(text, lang_code):
    try:
        translator = Translator()
        translated_text = translator.translate(
            text, src=lang_code, dest='en').text
        return translated_text
    except:
        return "Translation Failed"


def example_tamil():
    stext = "மோசமான பராமரிப்பால்  கோபமாக உணர்கிறேன்"  # "மிக மிக மோசமான பராமரிப்பு"

    [lcode, language] = detect_indian_language(stext)
    print(f"Original text: {stext}")
    print(f"The detected Indian language is: {language}")
    if (lcode != 'en'):
        translated_text = translate_to_english(stext, lcode)
        print(f"Translated text: {translated_text}")
