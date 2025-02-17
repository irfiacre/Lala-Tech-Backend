from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework import status
from api.serializer import UsersSerializer
from api.models import Users
from rest_framework.decorators import api_view


# firsname, lastname, role, email, {"firstname":"Kanakuze", "lastname": "Dativa", "role":"renter", "email": "kanakuze@dativa.com"}

@api_view(["POST"])
def register_user_view(request):
    result = None
    try:
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            result = serializer.data
    except Exception as err:
        return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(result, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def find_user_view(request, pk):
    try:
        result = Users.objects.get(email=pk)
        user_info = UsersSerializer(result)
    except user_info.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(user_info.data, status=status.HTTP_200_OK)
