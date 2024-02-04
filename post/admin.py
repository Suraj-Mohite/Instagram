from django.contrib import admin
from .models import Post, Tag, Follow, Stream, PostImage

# Register your models here.

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]

admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Stream)