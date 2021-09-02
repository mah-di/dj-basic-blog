from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .serializers import RegistrationSerializer, UserSerializer, UserProfileSerializer 


@api_view(['POST',])
@authentication_classes([])
@permission_classes([])
def registration_api(request):
    serialize = RegistrationSerializer(data=request.data)

    data = {}
    if serialize.is_valid():
        registered_user = serialize.save()
        print(registered_user)
        token = Token.objects.get(user=registered_user).key
        data['response'] = 'success'
        data['success'] = 'registration successful'
        data['token'] = token
        state= status.HTTP_201_CREATED
    else:
        data['response'] = 'error'
        data['errors'] = serialize.errors
        state= status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=state)


@api_view(['GET',])
def profile_api_view(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return Response({'response': 'error', 'errors': "user doesn't exist"}, status.HTTP_404_NOT_FOUND)
    
    serialize_user = UserSerializer(user)
    serialize_profile = UserProfileSerializer(user.user_profile)
    return Response(data={'user': serialize_user.data, 'profile': serialize_profile.data}, status=status.HTTP_200_OK)


@api_view(['GET','PUT',])
def profile_update_api_view(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response({'response': 'error', 'errors': "unauthorized request"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        serialize_user = UserSerializer(instance=user)
        serialize_profile = UserProfileSerializer(instance=user.user_profile)

        return Response(data={'user': serialize_user.data, 'profile': serialize_profile.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        allowed_keys = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_pic')
        data = {}
        if any(key in request.data for key in allowed_keys):
            serialize_user = UserSerializer(instance=user, data=request.data)
            serialize_profile = UserProfileSerializer(instance=user.user_profile, data=request.data)

            if serialize_profile.is_valid() and serialize_user.is_valid():
                serialize_user.save()
                serialize_profile.save()
                data['response'] = 'success'
                data['success'] = 'profile updated'
                state = status.HTTP_200_OK
            else:
                data['response'] = 'error'
                data['errors']={'user': serialize_user.errors, 'profile': serialize_profile.errors}
                state = status.HTTP_400_BAD_REQUEST
        else:
            data['response'] = 'error'
            data['errors'] = 'no valid data submited'
            state = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=state)
