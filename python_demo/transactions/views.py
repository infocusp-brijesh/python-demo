from django.http import JsonResponse
from rest_framework.decorators import api_view
from bank_accounts.models import Bank_Account
from user.models import Users
import jwt
from django.conf import settings

@api_view(['POST'])
def transfer_money(request):
    if (request.method == 'POST'):
        try:
            decoded_token = jwt.decode(str(request.headers['Authorization']).replace('Bearer ', ''), settings.SECRET_KEY, algorithms=['HS256'])
            user_data = Users.objects.get(pk=decoded_token['user_id'])

        except Bank_Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'jwt unauthorized'}, status=401)
        try:
            body = request.data
            
            required_keys = ['amount', 'self_account_no', 'transfer_account_no']
            
            for keys in required_keys:
                if (keys not in body or body[keys] == ''):
                    return JsonResponse({ 'message': keys + ' Required' }, status=419)
                
            if (body['amount'] < 0):
                    return JsonResponse({ 'message': 'Invalid transfer amount' }, status=419)
            
            if (body['self_account_no'] == body['transfer_account_no']):
                return JsonResponse({'message': 'Invalid account no'})
            
            accounts = Bank_Account.objects.filter(pk__in=[body['self_account_no'], body['transfer_account_no']])
            
            if (len(accounts) != 2):
                return JsonResponse({ 'error': 'Invalid account no' })
            
            self_account = None
            transfer_account = None
            
            # for account in accounts:
                
            return JsonResponse({ 'message': 'Amount transferred Successfully' })
        except Exception as e:
            print('Something Went Wrong', e)
            return JsonResponse({ 'message': 'Something went wrong' }, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, 405)
        
@api_view(['POST'])
def debit_money(request):
    pass

@api_view(['POST'])
def credit_money(request):
    pass

def get_transactions(request):
    return JsonResponse({ 'message': 'User Fetched Successfully' })
