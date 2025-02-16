from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Users
from ..serializer import UsersSerializer
from django.contrib.auth.hashers import make_password


# {"firstname": "john", "lastname":"doe","username":"jdoe","password":"12345"}

@api_view(["GET"])
def get_users(request):
    users=Users.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def register_user(request):
    request.data['password']=make_password(request.data['password'])
    if 'photo_url' not in request.data:
        request.data['photo_url'] = f'https://ui-avatars.com/api/?name={request.data['firstname']}+{request.data['lastname']}&background=random'
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, pk):
    try:
        user = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsersSerializer(user)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        Users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
