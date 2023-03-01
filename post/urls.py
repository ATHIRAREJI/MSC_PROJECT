from django.urls import path
from post.views import Index, NewPost,PostDetails,Tags

urlpatterns = [
    path('', Index, name='index'),
    path('new_post/', NewPost, name="new_post"),
    path('<uuid:post_id>', PostDetails, name="postdetails"),
    path('tag:<slug:tag_slug>', Tags, name='tags')
]
