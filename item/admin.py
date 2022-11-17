from django.contrib import admin
from .models import Item,Seller,Category,Tag,Comment


admin.site.register(Item)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)

class SellerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Seller, SellerAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Tag,TagAdmin)

admin.site.register(Comment)


# Register your models here.
