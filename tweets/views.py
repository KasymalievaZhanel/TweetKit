from random import randint
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404

from tweets.serializers import (
    TweetSerializer, 
    TweetCreateSerializer, 
    TweetActionSerializer
)
from .models import Tweet
from .forms import TweetForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    data = request.POST or None
    serializer = TweetCreateSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status = 400)  

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    obj = Tweet.objects.all()
    serializer = TweetSerializer(obj, many=True)
    return Response(serializer.data) 

@api_view(['GET'])
def tweets_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)   

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed"}, status=200) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
            
    return Response({}, status=200)

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)    

#pure_django
# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# def tweets_detail_view_pure_django(request, tweet_id, *args, **kwargs):
#     data = {
#     "id": tweet_id,
#     #"image_path": obj.image
#     }
#     status = 200
#     try:
#         obj = Tweet.objects.get(id = tweet_id)
#         data['content'] = obj.content
#     except:
#         data['massage'] = 'Not Found'
#         status = 404

#     return JsonResponse(data, status=status)


# # Create new view pure
# def tweet_create_view_pure_django(request, *args, **kwargs):
#     user = request.user
#     if not request.user.is_authenticated:
#         user = None
#         if is_ajax(request):
#             return JsonResponse({}, status=401)
#         return redirect(settings.LOGIN_URL)

#     form = TweetForm(request.POST or None)
#     next_url = request.POST.get("next") or None
#     print("next_url", next_url)

#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = user
#         # что- то там делаем 
#         obj.save()
#         if is_ajax(request):
#             if is_ajax(request):
#                 return JsonResponse(obj.serialize(), status=201)
#         if(next_url != None and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=settings.ALLOWED_HOSTS)):
#             return redirect(next_url)
#         form = TweetForm()
#     if form.errors:
#         return JsonResponse(form.errors, status=400)    
#     return render(request, 'components/form.html', context={"form":form})

# def tweet_list_view_pure_django(request, *args, **kwargs):
#     qs = Tweet.objects.all()
#     tweets_list= [x.serialize() for x in qs]
#     data = {
#         "isUser": False,
#         "response": tweets_list
#     }
#     return JsonResponse(data) 