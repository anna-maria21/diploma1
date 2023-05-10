from django.shortcuts import render
from django.http import HttpResponse
from playground.services import validator
from playground.services import helper
from playground.services import working_with_db


def start(request):
    return render(request, 'start.html', {'isStartPage': True})

def sendText(request):
    if request.method == 'POST':
        url = request.POST['input']
        foundedDocument = working_with_db.findByUrl(url)
        context = {}
        if foundedDocument is None:
            if validator.validate(url):
                processingResult = helper.processData(url)
                if processingResult['isURLOpenError']:
                    return render(request, 'sendText.html', {'isStartPage': False, 'isAnyError': True, 'enteredUrl': url, 'errorText': 'Ця url-адреса не може бути відкрита'})
                else:
                    foundedDocument = working_with_db.findByUrl(url)
                    context = {
                        'labels': foundedDocument['labelsOrder'],
                        'scores': foundedDocument['scores'],
                        'text': foundedDocument['text'],
                        'url': foundedDocument['url']
                    }
                    return render(request, 'resultPage.html', context)
            else:
                return render(request, 'sendText.html', {'isStartPage': False, 'isAnyError': True, 'enteredUrl': url, 'errorText': 'Невірна url-адреса'})
        else: 
            
            context = {
                'labels': foundedDocument['labelsOrder'],
                'scores': foundedDocument['scores'],
                'text': foundedDocument['text'],
                'url': foundedDocument['url']
            }
            return render(request, 'resultPage.html', context)
    return render(request, 'sendText.html', {'isStartPage': False, 'isAnyError': False}) 



