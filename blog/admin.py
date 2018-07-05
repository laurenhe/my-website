from django.contrib import admin
from .models import Post, Comment, Category, Contact
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdmin(admin.ModelAdmin):

	model = Post
	fields = ('title', 'slug', 'author', 'content', 'pic_url',
			  'created_date', 'published_date',)
	#prepopulated_fields = {'slug': ('title',)}
	readonly_fields = ('slug',)
	list_display = ('title', 'created_date', 'author', 'published_date',)

	class Media:
		widgets = {
            'content': CKEditorUploadingWidget(),
        }
		js = (
			'/static/js/jquery-2.2.4.min.js',
			'/static/ckeditor/ckeditor.js',
			'/static/js/custom.js',
		)
		css = {
            'all': ('/static/css/custom.css',)
        }

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'message')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
