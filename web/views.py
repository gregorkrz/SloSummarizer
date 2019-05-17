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
        if not (100000 >= len(tts) > 0):
            return HttpResponse('Dolžina besedila mora biti med 1 in 100000 znaki.')
        template = loader.get_template('output.html')
        summarized_text =  summarize(tts, nus, method=request.POST.get("method", "sum"), lang=request.POST.get("lang", "si"))
        comparison_percent = int(round((len(tts)-len(summarized_text))*100/len(tts)))
        if comparison_percent < 0: comparison_percent = 0 # whoops
        return HttpResponse(template.render({
            'tts': summarized_text,
            'percent': comparison_percent,
            'lang': request.POST.get("lang", "si")
            }))
    else:
        return redirect('/')