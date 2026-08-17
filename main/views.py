from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Post, Comment, Follow


@login_required
def home(request):

    if request.method == "POST":

        if "content" in request.POST:
            content = request.POST["content"]

            if content:
                Post.objects.create(
                    user=request.user,
                    content=content
                )

        elif "like" in request.POST:
            post = Post.objects.get(
                id=request.POST["post_id"]
            )

            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)

        elif "comment" in request.POST:
            post = Post.objects.get(
                id=request.POST["post_id"]
            )

            content = request.POST["comment"]

            if content:
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    content=content
                )

        return redirect("home")

    posts = Post.objects.all().order_by("-created_at")

    following_ids = request.user.following.values_list(
        "following_id",
        flat=True
    )

    suggestions = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=following_ids
    )[:5]

    return render(
        request,
        "main/home.html",
        {
            "posts": posts,
            "suggestions": suggestions
        }
    )


@login_required
def users(request):

    search = request.GET.get("search", "")

    all_users = User.objects.exclude(
        id=request.user.id
    ).prefetch_related(
        "followers",
        "following",
        "post_set"
    )

    if search:
        all_users = all_users.filter(
            username__icontains=search
        )

    return render(
        request,
        "main/users.html",
        {
            "users": all_users,
            "search": search
        }
    )

@login_required
def follow_user(request, user_id):

    user_to_follow = User.objects.get(
        id=user_id
    )

    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).first()

    if follow:
        follow.delete()
    else:
        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect("users")


@login_required
def profile(request, user_id):

    profile_user = User.objects.get(
        id=user_id
    )

    user_posts = Post.objects.filter(
        user=profile_user
    ).order_by("-created_at")

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    return render(
        request,
        "main/profile.html",
        {
            "profile_user": profile_user,
            "user_posts": user_posts,
            "followers_count": followers_count,
            "following_count": following_count,
        }
    )