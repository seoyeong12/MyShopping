from django.db import models
from django.contrib.auth.models import User
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/item/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/item/category/{self.slug}'
    class Meta:
        verbose_name_plural = 'Categories'

class Seller(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) #판매자 계정
    name = models.CharField(max_length=10,unique=True) #판매자 이름
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    address = models.CharField(max_length=200) #주소
    phone = models.CharField(max_length=15) #연락처
    bnum = models.IntegerField() #사업자등록번호

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/item/seller/{self.slug}'

class Item(models.Model): #상품
    name = models.CharField(max_length=30) #상품명
    content = models.TextField() #설명
    price = models.IntegerField() #가격
    head_image = models.ImageField(upload_to='item/images/', blank=True) #이미지
    manufacturer = models.CharField(max_length=30) #제조사

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE) #판매자 다대일

    category = models.ForeignKey(Category, null=True, blank = True, on_delete=models.SET_NULL) #카테고리 다대일

    tags = models.ManyToManyField(Tag, blank=True) #태그 다대다

    def __str__(self):
        return f'[{self.pk}]{self.name}::{self.author} : {self.price} : {self.manufacturer} : {self.seller}'

    def get_absolute_url(self):
        return f'/item/{self.pk}/'

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.item.get_absolute_url()}#comment-{self.pk}'
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'

# Create your models here.
