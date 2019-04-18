from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
            'status','get_sharecnt')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    exclude = ("sharecnt",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
