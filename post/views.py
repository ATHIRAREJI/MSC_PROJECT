from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.urls import reverse

#Models
from post.models import Stream, Post, Tag, PostLikes
from comment.models import PostComment

#Forms
from post.forms import PostForm
from comment.forms import CommentForm

# Create your views here.
@login_required
def Index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = [post.post_id for post in posts]
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted_date')
    template = loader.get_template('index.html')

    context = {
        'post_items': post_items
    }

    return HttpResponse(template.render(context, request))

@login_required
def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user.id

    # Comment section 
    comments = PostComment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            PostComment(comment=comment, post_id = post_id, user_id = user).save()
            #comment = form.save(commit=False)
            #comment.post = post
            #comment.user = user
            #commentObj.save()
            return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    else:
        form = CommentForm()

    template = loader.get_template('post_detail.html')
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }

    return HttpResponse(template.render(context, request))


@login_required
def NewPost(request):
    user = request.user.id
    tags_objects = []

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES )
        if form.is_valid():
            post_picture = form.cleaned_data.get('post_picture')
            caption = form.cleaned_data.get('post_caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))
            for tag in tags_list:
                t,created = Tag.objects.get_or_create(title=tag)
                tags_objects.append(t)

            p, created = Post.objects.get_or_create(post_picture = post_picture, post_caption = caption, user_id = user)
            p.tags.set(tags_objects)
            p.save()
            return redirect('index')
    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'new_post.html', context)


@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted_date')

    template = loader.get_template('tag.html')

    context = {
        'posts': posts,
        'tag': tag
    }

    return HttpResponse(template.render(context, request))

@login_required
def PostLike(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    no_of_current_likes = post.likes

    liked_data = PostLikes.objects.filter(user=user, post=post).count()

    if not liked_data:
        PostLikes.objects.create(user=user, post=post)
        no_of_current_likes +=1
    else:
        PostLikes.objects.filter(user=user, post=post).delete()
        no_of_current_likes -=1

    post.likes = no_of_current_likes
    post.save()

    return HttpResponseRedirect(reverse('postdetails',args=[post_id]))



