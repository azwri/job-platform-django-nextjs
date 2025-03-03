from django.shortcuts import render
from .serializers import SignUpSerialzer, UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerialzer(data=data)
    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user.save(password=make_password(data['password']))
            return Response({'message': 'User created successfully'}, status=201)
        else:
            return Response({'message': 'User already exists'}, status=400)
    else:
        return Response(user.errors, status=400)
    
