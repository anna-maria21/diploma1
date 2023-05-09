from playground.services import classificator
from playground.services import translator
from playground.services import parser


def processData(url):
    text = parser.prepare_data(url)
    if not text.get_error():
        translatedText = translator.translate(text.get_text())
        englishText = translatedText['translated_text']
        result = classificator.classify(englishText)
        return { 'isURLOpenError': False, 'result': result, 'text': text.get_text() }
    else:
        return { 'isURLOpenError': True }


def getFinalLabels(result):
    prevScore = result['scores'][0]
    finalLabels = [result['labels'][0]]
    for i in range(1, len(result['scores'])):
        if prevScore - result['scores'][i] < 0.05:
            prevScore = result['scores'][i]
            finalLabels.append(result['labels'][i])
    return finalLabels