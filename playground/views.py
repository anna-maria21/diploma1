from django.shortcuts import render, redirect
from django.http import HttpResponse
from playground.services import validator
from playground.services import helper

def start(request):
    return render(request, 'start.html', {'isStartPage': True})

def sendText(request):
    if request.method == 'POST':
        url = request.POST['input']
        if validator.validate(url):
            processingResult = helper.processData(url)
            if processingResult['isURLOpenError']:
                return render(request, 'sendText.html', {'isStartPage': False, 'isAnyError': True, 'enteredUrl': url, 'errorText': 'Ця url-адреса не може бути відкрита'})
            else:
                print(processingResult['result'])
                # finalLabels = helper.getFinalLabels(processingResult['result'])
                return render(request, 'resultPage.html', {'result': processingResult['result'], 'text': processingResult['text']})
        else:
            return render(request, 'sendText.html', {'isStartPage': False, 'isAnyError': True, 'enteredUrl': url, 'errorText': 'Невірна url-адреса'})
    return render(request, 'sendText.html', {'isStartPage': False, 'isAnyError': False}) 