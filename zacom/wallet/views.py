from django.shortcuts import redirect, render
from .models import Wallet, WalletTransaction
from orders.models import OrderProduct,Order
from customers.models import Account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import razorpay
import json
from django.views.decorators.cache import never_cache
from django.core.cache import cache

from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.conf import settings

# Create your views here.
@never_cache 
def wallet(request):

    if request.user.is_authenticated:
        user = request.user.id
        user_detail= Account.objects.get(id=user)
        print(user_detail)
        order_dtails=OrderProduct.objects.filter(user=user).count()
        wallet, created = Wallet.objects.get_or_create(user=user_detail, defaults={'balance': 0})
        print(wallet)
        transactions = WalletTransaction.objects.filter(wallet=wallet).order_by('-created_at')
        print(wallet.balance,'Wallet balance')
        context = {'wallet': wallet,
                'transactions': transactions,
                'user_detail':user_detail,
                'order_dtails':order_dtails,}


        if request.method == 'POST':
            currency = 'INR'
            amount = int(json.loads(request.body)['amount']) 
            print(amount,user,currency)
            data = {'amount': amount}
            serialized_data = json.dumps(data)
            cache.set('payment_data', serialized_data)
            client = razorpay.Client(auth=("rzp_test_vAeyohaspEahRA", "076FQiZmu52B1ODs1UWKe2HF"))


            print('==========fff==============')
            try:
            
                data = {
                    'amount':(int(amount)* 100),
                    'currency':'INR',
                }
                payment1 = client.order.create(data=data)
                print(payment1)
                payment_order_id = payment1['id']
                context = {
                    'amount': amount,
                    'payment_order_id': payment_order_id,
                    'RAZOR_PAY_KEY_ID':'rzp_test_vAeyohaspEahRA'
                }
                return JsonResponse(context)
            except Exception as e:
                print('Error creating Razorpay order:', str(e))
                return JsonResponse({'error': 'Internal Server Error'}, status=500)
            
        return render(request,'dashboard/wallet.html',context)
    return redirect("home") 


@csrf_exempt
def paymenthandler2(request):
    print("Payment Handler endpoint reached")
    user = request.user
    if request.method == "POST":
        try:
            payment_id        = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature         = request.POST.get('razorpay_signature', '')
            print(f'1:{payment_id},2:{razorpay_order_id},3:{signature}')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            } 
            client = razorpay.Client(auth=("rzp_test_vAeyohaspEahRA", "076FQiZmu52B1ODs1UWKe2HF"))
            result = client.utility.verify_payment_signature(params_dict)
            if not result :
                return render(request, 'paymentfail.html')
            else:
                amount = int(request.GET.get('amount'))
                user_id = request.GET.get('user_id')
                if amount:
                    user= Account.objects.get(id=user_id)
                    wallet=Wallet.objects.get(user=user)
                    wallet.balance += amount
                    WalletTransaction.objects.create(wallet=wallet, amount=amount, transaction_type='CREDIT')
                    wallet.save()
                    return redirect('wallet')  
                else:
                    return render(request, 'order_templates/paymentfail.html')
        except Exception as e:
            print('Exception:', str(e))
            return render(request, 'order_templates/paymentfail.html')
    else:
        return redirect('shop')