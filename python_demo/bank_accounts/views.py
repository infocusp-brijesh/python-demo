from django.http import JsonResponse
from rest_framework.decorators import api_view
import jwt
from .models import Users, Bank_Account
from django.conf import settings

def health_check(request):
    return JsonResponse({ 'message': 'Success' })

def create_bank_account(request, user_data):
    try:
        body = request.data
        
        required_keys = ['account_type', 'balance']
        
        for keys in required_keys:
            if (keys not in body or body[keys] == ''):
                return JsonResponse({ 'message': keys + ' Required' }, status=419)
            
        if (body['balance'] < 0):
                return JsonResponse({ 'message': 'Invalid balance amount' }, status=419)
            
        account_type_enum = ['sa', 'cu']
        
        if body['account_type'] not in account_type_enum:
            return JsonResponse({"error": "Invalid account type"}, status=400)

        if Bank_Account.objects.filter(account_type=body['account_type'], user_id=user_data.id).exists():
            return JsonResponse({"error": "Account already exists"}, status=400)
        
        body_account_data = Bank_Account(user = user_data, current_balance = body['balance'], account_type = body['account_type'])
        
        body_account_data.save()
        return JsonResponse({ 'message': 'Bank Account Created Successfully' })
    except Exception as e:
        print('Something Went Wrong', e)
        return JsonResponse({ 'message': 'Something went wrong' }, status=500)

def get_bank_accounts(request, user_data):
    try:
        decoded_token = jwt.decode(str(request.headers['Authorization']).replace('Bearer ', ''), settings.SECRET_KEY, algorithms=['HS256'])
        account_data = Bank_Account.objects.filter(user_id=decoded_token['user_id'])
    except Bank_Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'jwt unauthorized'}, status=401)
    
    response_data = []
    
    for account in account_data:
        temp_dir = {
            'account_type': account.account_type,
            'balance': account.current_balance,
            'last_updated_at': account.updated_at
        }
        response_data.append(temp_dir)

    response_user_data = {
        'id': user_data.id,
        'user_name': user_data.user_name,
        'email': user_data.email,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
    }
    return JsonResponse({'message': 'User data fetched successfully', 'data': { 'user_data': response_user_data, 'accounts': response_data }}, status=200)

@api_view(['GET', 'POST'])
def handle_bank_account(request):
    try:
        decoded_token = jwt.decode(str(request.headers['Authorization']).replace('Bearer ', ''), settings.SECRET_KEY, algorithms=['HS256'])
        user_data = Users.objects.get(pk=decoded_token['user_id'])

    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'jwt unauthorized'}, status=401)

    if request.method == "GET":
        return get_bank_accounts(request, user_data)
    elif request.method == "POST":
        return create_bank_account(request, user_data)
    else:
        return JsonResponse({ 'message': 'Method Not Allowed' }, status=405)
