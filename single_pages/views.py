from django.shortcuts import render
def about_me(request):
    return render(request, 'single_pages/about_me.html')
def about_us(request):
    return render(request, 'single_pages/about_us.html')
# Create your views here.
