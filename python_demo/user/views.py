import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Users
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt

def create_user(request): 
    try:
        body = request.data

        required_keys = ['user_name', 'first_name', 'email', 'password', 'phone_number']

        for keys in required_keys:
            if (keys not in body or body[keys] == ''):
                return JsonResponse({ 'message': keys + ' Required' }, status=419)
        
        if Users.objects.filter(email=body['email']).exists():
            return JsonResponse({"error": "Email already in use"}, status=400)

        if Users.objects.filter(user_name=body['user_name']).exists():
            return JsonResponse({"error": "User Name already in use"}, status=400)
        
        if Users.objects.filter(phone_number=body['phone_number']).exists():
            return JsonResponse({"error": "Phone Number already in use"}, status=400)
        
        body_userdata = Users(first_name = body['first_name'], last_name = body['last_name'], user_name = body['user_name'], email = body['email'], email_verified = True, phone_number = body['phone_number'], phone_verified = True, password = make_password(body['password']))
        
        body_userdata.save()
        
        return JsonResponse({ 'message': 'User Created Successfully' })
    except Exception as e:
        print('Something Went Wrong', e)
        return JsonResponse({ 'message': 'Something went wrong' }, status=500)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_user(request):
    try:
        decoded_token = jwt.decode(str(request.headers['Authorization']).replace('Bearer ', ''), settings.SECRET_KEY, algorithms=['HS256'])
        user_data = Users.objects.get(pk=decoded_token['user_id'])

    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'jwt unauthorized'}, status=401)
    response_user_data = {
        'id': user_data.id,
        'user_name': user_data.user_name,
        'email': user_data.email,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
    }

    return JsonResponse({'message': 'User data fetched successfully', 'data': response_user_data}, status=200)

@api_view(['GET', 'POST'])
def handle_user(request):
    if request.method == "GET":
        return get_user(request)
    elif request.method == "POST":
        return create_user(request)

@api_view(['POST'])
def login(request):
    if request.method == "POST":
        body = request.data
        try:
            user_data = Users.objects.get(user_name=body['user_name'])
            if(check_password(body['password'], user_data.password) == False):
                return JsonResponse({'error': 'Username or password incorrect'}, status=401)
        except Users.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        token = get_tokens_for_user(user_data)

        response_user_data = {
            'token': token
        }
        
        user_data.token = token['access']
        
        user_data.save()
                
        return JsonResponse({ 'message': 'User Login Successfull', 'data': response_user_data }, status=200)
    else:
        return JsonResponse({ 'message': 'Method Not Allowed' }, status=405)
    