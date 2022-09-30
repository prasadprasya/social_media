from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
import jwt
from social_media.settings import SECRET_KEY
import logging
from datetime import datetime, timedelta
from social_media import settings

# Create your views here.

logger = logging.getLogger("Views file API's")


@api_view(['POST'])
def register(request):
    email = request.data.get('email', "").lower().strip()
    password = request.data.get('password')
    re_enter_password = request.data.get('re_enter_password')
    response_data = {"status": False}
    try:
        Users.objects.get(email=email)
        response_data['response'] = "User already registered with same email"
    except Users.DoesNotExist:
        user_name = email.split("@")[0]
        if password != re_enter_password:
            response_data['response'] = "Passwords must match"
            response_data['email'] = email
            response_data["status"] = False
        else:
            user_obj = Users.objects.create(email=email, user_name=user_name,
                                            password=password)

            # token = RefreshToken.for_user(user).access_token
            jwt_payload = dict()
            jwt_payload['user_id'] = str(user_obj.id)
            jwt_payload['email'] = email
            jwt_payload['username'] = user_name
            tomorrow_date = datetime.now() + timedelta(hours=24)
            jwt_payload['exp'] = tomorrow_date
            # print(jwt_payload)
            token = jwt.encode(
                jwt_payload, settings.SECRET_KEY, algorithm="HS256")
            response_data["status"] = True
            response_data["response"] = "registered Successfully"
            response_data["token"] = token
    return Response(response_data)


@api_view(['POST'])
def authenticate(request):
    email = request.data.get("email", None)
    password = request.data.get("password", None)
    response_data = {"response": "", "status": False}
    try:
        user_obj = Users.objects.get(email=email)
        if user_obj.password:
            is_password_valid = True if password == user_obj.password else False
        else:
            is_password_valid = False

        if is_password_valid:
            jwt_payload = dict()
            jwt_payload['user_id'] = str(user_obj.id)
            jwt_payload['email'] = email
            jwt_payload['password'] = password
            token = jwt.encode(
                jwt_payload, SECRET_KEY, algorithm="HS256")
            response_data["token"] = token
            response_data["response"] = "User Authenticated Successfully"
            response_data["status"] = True
        else:
            response_data["response"] = "InCorrect Password/User Not Found"
    except Users.DoesNotExist:
        response_data["response"] = "User Not Found"
    except BaseException as e:
        logger.info(f"authenticate  is failed due to error msg----->{e}")
    return Response(response_data)


@api_view(['GET'])
def user(request):
    login_user_id = request.headers.user_id
    response_data = {"data": {}, "response": "", "status": False}
    try:
        user_obj = Users.objects.get(id=login_user_id)
        response_data["data"] = {"user_name": user_obj.user_name,
                                 "followers": [], "following": []}
        if user_obj:
            followers_obj = Followers.objects.filter(follower=login_user_id)
            for follower in followers_obj:
                response_data["data"]["followers"].append({"user_name": follower.follower.user_name})

            following_obj = Followers.objects.filter(following_to=login_user_id)
            for following in following_obj:
                response_data["data"]["following"].append({"user_name": following.following_to.user_name})
        response_data["response"] = "Data Retrieved Successfully"
        response_data["status"] = True

    except Users.DoesNotExist:
        response_data["response"] = "User Not Found"
    except BaseException as e:
        logger.info(f"user is failed due to error msg----->{e}")
    return Response(response_data)


@api_view(['DELETE', 'GET'])
def posts(request, post_id):
    login_user_id = request.headers.user_id
    if request.method == 'GET':
        response_data = {"data": {}, "response": "", "status": False}
        try:
            post_obj = Posts.objects.get(id=post_id)
            response_data["data"] = {"post_id": post_obj.id, "title": post_obj.title,
                                     "description": post_obj.description,
                                     "created_time": post_obj.created_date}
            response_data["response"] = "Data retrieved Successfully"
            response_data["status"] = True
        except Posts.DoesNotExist:
            response_data["response"] = "Post Not Found"
        except BaseException as e:
            logger.info(f"posts is failed due to error msg----->{e}")
        return Response(response_data)

    if request.method == 'DELETE':
        response_data = {"response": "", "status": False}
        try:
            post_obj = Posts.objects.get(id=post_id)
            post_obj.delete()
            response_data["response"] = "Deleted Successfully"
            response_data["status"] = True
        except Posts.DoesNotExist:
            response_data["response"] = "Post Not Found"
        except BaseException as e:
            logger.info(f"posts is failed due to error msg----->{e}")
        return Response(response_data)


@api_view(['POST'])
def create_post(request):
    login_user_id = request.headers.user_id
    title = request.data.get("title", None)
    description = request.data.get("description", None)
    response_data = {"data": {}, "response": "", "status": False}
    try:
        user_obj = Users.objects.get(id=login_user_id)
        post_obj = Posts.objects.create(title=title, description=description, created_by=user_obj)
        response_data["data"] = {"post_id": post_obj.id, "title": post_obj.title,
                                 "description": post_obj.description,
                                 "created_time": post_obj.created_date}
        response_data["response"] = "Created Successfully"
        response_data["status"] = True
    except Posts.DoesNotExist:
        response_data["response"] = "Post Not Created"
    except BaseException as e:
        logger.info(f"posts is failed due to error msg----->{e}")
    return Response(response_data)


@api_view(['GET'])
def all_posts(request):
    login_user_id = request.headers.user_id
    response_data = {"data": [], "response": "", "status": False}
    try:
        post_obj = Posts.objects.filter(created_by=login_user_id)
        for post in post_obj:
            post_data_dict = {"post_id": post.id, "title": post.title,
                              "description": post.description,
                              "created_at": post.created_date,
                              "comments": [], "likes": 0}
            comment_obj = Comments.objects.filter(post_id=post)
            for com in comment_obj:
                post_data_dict["comments"].append({"comment": com.comment, "comment_by": com.commented_by.user_name})
            like_obj = Likes.objects.filter(post_id=post)
            post_data_dict["likes"] = len(like_obj)
            response_data["data"].append(post_data_dict)
        response_data["response"] = "Data retrieved Successfully"
        response_data["status"] = True
    except BaseException as e:
        logger.info(f"all_posts is failed due to error msg----->{e}")
    return Response(response_data)


@api_view(['POST'])
def follow(request, following_to_id):
    # follow_uuid = request.data.get("follow_uuid", None)
    login_id = request.headers.user_id
    response_data = {"response": "", "status": False}
    if following_to_id:
        try:
            if login_id == following_to_id:
                response_data["response"] = "User Not Allowed to follow Him self"
            else:
                follower_obj = Followers.objects.get(follower=login_id, following_to=following_to_id)
                response_data["response"] = "User Already Followed"
        except Followers.DoesNotExist:
            try:
                user_obj = Users.objects.get(id=login_id)
                follow_obj = Users.objects.get(id=following_to_id)
                follower_obj = Followers.objects.create(follower=user_obj, following_to=follow_obj)
                response_data["response"] = "User Followed Successfully"
                response_data["status"] = True
            except Users.DoesNotExist:
                response_data["response"] = "User Not Found"
        except BaseException as e:
            logger.info(f"follow is failed due to error msg----->{e}")
    else:
        response_data["response"] = "Provide following person id "
    return Response(response_data)


@api_view(['POST'])
def unfollow(request, following_to_id):
    login_id = request.headers.user_id
    response_data = {"response": "", "status": False}
    try:
        follower_obj = Followers.objects.get(follower=login_id, following_to_id=following_to_id)
        follower_obj.delete()
        response_data["response"] = "Unfollowed Successfully"
        response_data["status"] = True
    except Followers.DoesNotExist:
        response_data["response"] = "User Not in Followers List"
    except BaseException as e:
        logger.info(f"unfollow is failed due to error msg----->{e}")
    return Response(response_data)


@api_view(['POST'])
def like(request, post_id):
    login_id = request.headers.user_id
    response_data = {"response": "", "status": False}
    try:
        Likes.objects.get(post_id=post_id, liked_by=login_id)
        response_data["response"] = "Already Liked"
        response_data["status"] = True
    except Likes.DoesNotExist:
        try:
            liked_by = Users.objects.get(id=login_id)
            post_obj = Posts.objects.get(id=post_id)
            like_obj = Likes.objects.create(post_id=post_obj, liked_by=liked_by)
            response_data["response"] = "User Liked Successfully"
            response_data["status"] = True
        except Posts.DoesNotExist:
            response_data["response"] = "Post Not Found"
    except BaseException as e:
        logger.info(f"like is failed due to error msg----->{e}")
    return Response(response_data)


@api_view(['POST'])
def unlike(request, post_id):
    login_id = request.headers.user_id
    response_data = {"response": "", "status": False}
    try:
        like_obj = Likes.objects.get(post_id=post_id, liked_by=login_id)
        like_obj.delete()
        response_data["response"] = "Unliked Successfully"
        response_data["status"] = True
    except Likes.DoesNotExist:
        response_data["response"] = "User Not Liked"
    except BaseException as e:
        logger.info(f"unlike is failed due to error msg----->{e}")
    return Response(response_data)


@api_view(['POST'])
def comment(request, post_id):
    login_id = request.headers.user_id
    comment = request.data.get("comment", None)
    response_data = {"response": "", "status": False}
    try:
        user_obj = Users.objects.get(id=login_id)
        post_obj = Posts.objects.get(id=post_id)
        comment_obj = Comments.objects.create(post_id=post_obj, commented_by=user_obj, comment=comment)
        response_data["response"] = "User Commented Successfully"
        response_data["status"] = True
        response_data["data"] = {"comment_id": comment_obj.id}
    except Posts.DoesNotExist:
        response_data["response"] = "Post Not Found"
    except BaseException as e:
        logger.info(f"comment is failed due to error msg----->{e}")
    return Response(response_data)

