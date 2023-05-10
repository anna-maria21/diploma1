from playground.services import classificator
from playground.services import translator
from playground.services import parser
from playground.services import working_with_db

def processData(url):
    text = parser.prepare_data(url)
    if not text.get_error():
        ukrainianText = text.get_text()
        translatedText = translator.translate(ukrainianText)
        englishText = translatedText['translated_text']
        result = classificator.classify(englishText)
        working_with_db.insertDocument(result, url, ukrainianText)
        return { 'isURLOpenError': False, 'text': text.get_text() }
    else:
        return { 'isURLOpenError': True }
