from django.shortcuts import render

def layout(request):
    return render(request, 'layout.html')

def start_screen(request):
    return render(request, 'startScreen.html')

def feed(request):
    return render(request, 'feed.html')