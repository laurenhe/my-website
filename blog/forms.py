from django import forms
from .models import Post, Comment, Contact
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.text import slugify


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ('title', 'content',)

    def clean_name(self):
        n = self.cleaned_data['title']
        if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
            raise ValidationError("Post name can't be '{}'".format(n))
        return n

    def clean(self):
        cleaned_data = super(PostForm, self).clean() # call the parent clean method
        title  = cleaned_data.get('title')
        import pdb; pdb.set_trace()
        # if title exists create slug from title
        if title:
            cleaned_data['slug'] = slugify(title)
        return cleaned_data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'message',)

    def clean_name(self):
        name = self.cleaned_data['name']
        name_l = name.lower()
        if name_l == "admin" or name_l == "author":
            raise ValidationError("Author name can't be 'admin/author'")
        return name

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Name"
        self.fields['email'].label = "Email"
        self.fields['message'].label = "Message"


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Name"
        self.fields['email'].label = "Email"
        self.fields['subject'].label = "Subject"
        self.fields['message'].label = "Message"
