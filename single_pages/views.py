from django.shortcuts import render,redirect
from item.models import Item,Comment
def landing(request):
    recent_items = Item.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_items' : recent_items,
        }
    )
def about_me(request):
    items = Item.objects.order_by('-pk')
    comments = Comment.objects.order_by('pk')
    if request.user.is_authenticated:
        return render(request, 'single_pages/about_me.html',{
            'items' : items,
            'comments' : comments
        })
    else:
        return redirect('/item/')
def about_us(request):
    return render(request, 'single_pages/about_us.html')
# Create your views here.
