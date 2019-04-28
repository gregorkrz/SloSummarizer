from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import redirect
from .summarizer import summarize


def index(request):
    template = loader.get_template('inputform.html')
    return HttpResponse(template.render(request=request))

def summary(request):
    if request.method == "POST":
        tts = request.POST.get("tts", "")
        nus = request.POST.get("nus", "5")
        nus = int(nus)
        if not (10000 >= len(tts) > 0):
            return HttpResponse('Dolžina besedila mora biti med 1 in 10000 znaki.')
        template = loader.get_template('output.html')
        return HttpResponse(template.render({'tts': summarize(tts, nus)}))
    else:
        return redirect('/')