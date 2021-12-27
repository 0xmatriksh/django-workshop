from django.contrib import admin
from .models import BlogPost,Category,Author

class PostAdminModel(admin.ModelAdmin):
    list_display = ('title','author', 'category','created_at')
    list_filter = ('created_at',)
    list_editable = ('category',)

# Register your models here.
admin.site.register(BlogPost,PostAdminModel)
admin.site.register(Category)
admin.site.register(Author)