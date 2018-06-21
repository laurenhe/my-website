from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, ContactForm
from django.contrib import messages


def post_detail(request, pk, post_slug):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.add_message(request, messages.INFO, 'Your message was added!')
            return redirect('post_detail', pk=post.pk, post_slug=post.slug)
        else:
            comment = CommentForm()
    else:
        comment = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment})

def add_comment(request, pk, post_slug):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.add_message(request, messages.INFO, 'Your message was added!')
            return redirect('post_detail', pk=post.pk, post_slug=post.slug)
    # if request is GET then show unbound form to the user
    else:
        comment = CommentForm()
    return render(request, 'blog/post_detail.html', {'comment_form': comment})


def post_cat(request):
    categories = Category.objects.all()
    return render(request, 'blog/post_cat.html', {'categories': categories})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            sender = form.cleaned_data['email']
            subject = "You have a new message from {}:{}".format(name, sender)
            message = "Subject: {}\n\nMessage: {}".format(f.cleaned_data['subject'], f.cleaned_data['message'])
            mail_admins(subject, message)
            form.save()
            messages.add_message(request, messages.INFO, 'Submitted!')
            return redirect('contact')
    else:
        contact = ContactForm()
    return render(request, 'blog/contact.html', {'contact_form': contact})

@login_required
def post_publish(request, pk, post_slug):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk, post_slug=post.slug)

@login_required
def post_edit(request, pk, post_slug):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk, post_slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk, post_slug=comment.post.slug)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk, post_slug=comment.post.slug)
