from playground.services import classificator
from playground.services import translator
from playground.services import parser
from playground.services import working_with_db

curUrl = ''


def processData(url):
    text = parser.prepare_data(url)
    if not text.get_error():
        ukrainianText = text.get_text()
        translatedText = translator.translate(ukrainianText)
        englishText = translatedText['result']
        resultBart = classificator.classifyBart(englishText)
        resultZeroShot = classificator.classifyZeroShot(englishText)
        resultRandomForest = classificator.classifyRandomForest(englishText)
        # resultRandomForest = ''
        working_with_db.insertDocument(resultBart, resultZeroShot, resultRandomForest, url, ukrainianText)
        return { 'isURLOpenError': False, 'text': text.get_text() }
    else:
        return { 'isURLOpenError': True }


def countAvgMark():
    documentMarks = working_with_db.findAll()
    sum = 0
    count = 0
    for mark in documentMarks:
        if mark != 0:
            sum += mark
            count += 1
    return round(sum / count, 3)