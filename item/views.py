from django.shortcuts import render
from .models import Item,Seller,Category,Tag
from django.views.generic import ListView, DetailView

class ItemList(ListView):
    model = Item
    ordering = '-pk'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['sellers'] = Seller.objects.all()
        context['no_seller_item_count'] = Item.objects.filter(seller=None).count
        return context


class ItemDetail(DetailView):
    model = Item
    def get_context_data(self,**kwargs):
        context = super(ItemDetail,self).get_context_data()  #위 함수와 super 매개변수의 차이
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['sellers'] = Seller.objects.all()
        context['no_seller_item_count'] = Item.objects.filter(seller=None).count
        return context


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        item_list = Item.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        item_list = Item.objects.filter(category=category)
    return render(request, 'item/item_list.html', {
        'category' : category,
        'item_list' : item_list,
        'categories' : Category.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count
    })
def seller_page(request, slug):
    if slug == 'no_seller':
        seller = '미분류'
        item_list = Item.objects.filter(seller=None)
    else :
        seller = Seller.objects.get(slug=slug)
        item_list = Item.objects.filter(seller=seller)
    return render(request, 'item/item_list.html', {
        'seller' : seller,
        'item_list' : item_list,
        'sellers' : Seller.objects.all(),
        'no_seller_item_count' : Item.objects.filter(seller=None).count
    })
def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug)
    item_list = tag.item_set.all()
    return render(request,'item/item_list.html',{
        'tag': tag,
        'item_list': item_list,
        'categories' : Category.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count,
        'sellers': Seller.objects.all(),
        'no_seller_item_count': Item.objects.filter(seller=None).count
    })
# Create your views here.

