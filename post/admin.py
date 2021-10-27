from django.contrib import admin
from .models import Post, Comment
from django.apps import AppConfig
# Register your models here.

class PostAdmin(admin.ModelAdmin):

    list_display = ['title', 'publishing_date', 'slug']
    list_display_links = ['publishing_date']
    list_filter = ['publishing_date']
    search_fields = ['title', 'content']
    list_editable = ['title']

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)

# Buradan asagisini test icin yazdim silebiliriz...
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment

    class FrontendConfig(AppConfig):
        verbose_name = 'Yorumlar'

    list_display = ['name', 'post', 'content', 'created_date', 'is_approved']

    verbose_name = 'Yorumlar'


admin.site.register(Comment, CommentAdmin)