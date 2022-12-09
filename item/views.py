from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST

from .models import Item,Seller,Category,Tag ,Comment
from django.views.generic import ListView, DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

class ItemUpdate(LoginRequiredMixin,UpdateView):
    model = Item
    fields = ['name','content','price','head_image','manufacturer','category'] #'tags'

    template_name = 'item/item_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    def form_valid(self, form):
        response = super(ItemUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemUpdate,self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name) #append 맨뒤에 하나씩 추가
            context['tags_str_default'] = ';'.join(tags_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['sellers'] = Seller.objects.all()
        context['no_seller_item_count'] = Item.objects.filter(seller=None).count
        return context
class ItemCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Item
    fields = ['name','content','price','head_image','manufacturer','category'] #'tags'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemCreate,self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str :
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',',';') #구분자 ,랑 ; 설정
                tags_list = tags_str.split(';') #시스템 내에서는 ;로 구분?
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/item/')
    #템플릿 : 모델명_form.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemCreate,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['sellers'] = Seller.objects.all()
        context['no_seller_item_count'] = Item.objects.filter(seller=None).count
        return context
class ItemList(ListView):
    model = Item
    ordering = '-pk'
    paginate_by = 5
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
        context['comment_form'] = CommentForm

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
        'no_category_item_count' : Item.objects.filter(category=None).count,
        'sellers': Seller.objects.all(),
        'no_seller_item_count': Item.objects.filter(seller=None).count
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
        'no_seller_item_count' : Item.objects.filter(seller=None).count,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count
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
def new_comment(request,pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item,pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: #GET
            return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied
class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    # CreateView, UpdateView, form을 사용하면
    #템플릿이 모델명_forms 자동생성 : comment_form
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    item = comment.item
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied


class ItemSearch(ItemList):
    paginate_by = None
    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(
            Q(name__contains=q) | Q(tags__name__contains=q) | Q(manufacturer__contains=q)
        ).distinct()
        return item_list
    def get_context_data(self, **kwargs):
        context = super(ItemSearch,self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context

@require_POST
def likes(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)

        if item.like_users.filter(pk=request.user.pk).exists():
            item.like_users.remove(request.user)
        else:
            item.like_users.add(request.user)
        return redirect(item.get_absolute_url())
    raise PermissionDenied
# def likes(request, pk):
#     if request.user.is_authenticated:
#         item = get_object_or_404(Item, pk=pk)
#
#         if item.like_users.filter(username=request.user.username).exists():
#             item.like_users.remove(request.user)
#         else:
#             item.like_users.add(request.user)
#         item.save()
#         return redirect(item.get_absolute_url())
#     raise PermissionDenied
