from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Users
from ..serializer import UsersSerializer
from ..utils import encodeJWT
from django.contrib.auth.hashers import check_password



# {"username":"jdoe", "password":"12345"}

@api_view(["POST"])
def user_login(request):
    try:
        username = request.data['username']
        password=request.data['password']
        user = Users.objects.get(username=username)
        userInfo = UsersSerializer(user).data
        if not check_password(password, userInfo['password']):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    access_token = encodeJWT(userInfo)
    response = Response(status=status.HTTP_200_OK)
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    response.data = {"access_token": access_token}

    return response
