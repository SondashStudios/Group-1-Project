# discussionboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import Post, Comment, CommentVote
from .forms import PostForm, CommentForm

from rest_framework import viewsets, permissions
from .serializers import PostSerializer, CommentSerializer

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'discussionboard/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('discussionboard:post_list')
    else:
        form = PostForm()
    return render(request, 'discussionboard/post_form.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('discussionboard:post_detail', args=[post.id]))
    else:
        comment_form = CommentForm()
    return render(request, 'discussionboard/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('discussionboard:post_detail', args=[post.id]))

@require_POST
@login_required
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    value = int(request.POST.get('value'))
    vote, created = CommentVote.objects.get_or_create(user=request.user, comment=comment)
    if not created and vote.value != value:
        vote.value = value
        vote.save()
    elif not created:
        vote.delete()
    else:
        vote.value = value
        vote.save()
    comment.score = sum(v.value for v in comment.votes.all())
    comment.save()
    return JsonResponse({'score': comment.score})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
