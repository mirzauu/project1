from decimal import Decimal
from django.shortcuts import render,redirect
from django.urls import reverse
from customers.models import Account,AdressBook
import json
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from cart.models import CartItem,Cart
from products.models import Product_Variant
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from .models import Payment,PaymentMethod,OrderProduct,Order,ReturnRequest
from wallet.models import Wallet,WalletTransaction
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import razorpay

@method_decorator(login_required, name='dispatch')
class Review(View):
    
    def get(self,request):
        
    # if the cart count is less than or equal to 0 ,then redirect back to shop
        
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        cart_count = cart_items.count()
        if cart_count < 0:
            return redirect('shop')
        

        
        total_with_orginal_price =0
        total = 0
        quantity=0

        try:
        
                cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    
                print(cart_items)
                for cart_item in cart_items:
                    total += cart_item.sub_total()
                    # total += ( cart_item.product.sale_price * cart_item.quantity)
                    total_with_orginal_price += ( cart_item.product.max_price * cart_item.quantity)
                    quantity += cart_item.quantity

                    if cart_item.quantity > cart_item.product.stock:
                        messages.error(request, f"Insufficient stock for {cart_item.product}")
                        return render(request, 'user_templates/order_summary.html', {'cart_items': cart_items})
                    
            
        except ObjectDoesNotExist:
            pass
        
        
        Discount = request.session.get('discount', Decimal('0')) 
        total_float = float(total)
        Discount_float = float(Discount)

        grandtotal = total_float - Discount_float
    

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'grand_total':grandtotal,
            'discount':Discount,
            'total_with_orginal_price':total_with_orginal_price
        }
        
        return render (request,'user_templates/order_summary.html',context)



@method_decorator(login_required, name='dispatch')
class Address(View):
    
    
    def get(self,request):

        user = request.user.id
        address = AdressBook.objects.filter(user=user)
        cart_items = CartItem.objects.filter(user=user,is_active=True)

        if cart_items.count()>=1:


            total_with_orginal_price =0
            total=0
            quantity=0

            
            for cart_item in cart_items:
                total += cart_item.sub_total()
                # total += ( cart_item.product.sale_price * cart_item.quantity)
                total_with_orginal_price += ( cart_item.product.max_price * cart_item.quantity)
                quantity += cart_item.quantity

                

            Discount = request.session.get('discount', Decimal('0')) 
            total_float = float(total)
            Discount_float = float(Discount)

            grandtotal = total_float - Discount_float


            context = {'adress': address,
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'grand_total':grandtotal,
            'discount':Discount,
            'total_with_orginal_price':total_with_orginal_price}


            return render (request,'user_templates/order-address.html',context)
        
        else:

            return render (request,'user_templates/home.html')

    def post(self,request): 
        
        user = request.user.id
        data = json.loads(request.body)
        if selected_address_id := data.get('addressId'):
            try:
                selected_address = AdressBook.objects.get(pk=selected_address_id)
                selected_address.is_default = True
                selected_address.save()

                # Update other addresses to set is_default=False
                AdressBook.objects.filter(user=user).exclude(pk=selected_address_id).update(is_default=False)

                return JsonResponse({'success': True, 'message': 'Address set as default successfully'})
            except AdressBook.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Selected address not found'})
            
        else:
            return JsonResponse({'success': False, 'message': 'No address ID provided'})
        

@method_decorator(login_required, name='dispatch')
class Paymentt(View):
   
    def get(self, request):
        user = request.user.id
        user_detail= Account.objects.get(id=user)
        wallet, created = Wallet.objects.get_or_create(user=user_detail,defaults={'balance': 0})
        cart_items = CartItem.objects.filter(user=user, is_active=True)

    
        if cart_items.count()>=1:

            total_with_original_price = 0
            total = 0
            quantity = 0

            for cart_item in cart_items:
                total += cart_item.sub_total()
                total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
                quantity += cart_item.quantity

            Discount = request.session.get('discount', Decimal('0')) 
            total_float = float(total)
            Discount_float = float(Discount)

            grandtotal = total_float - Discount_float
    

            context = {

                'total': total,
                'quantity': quantity,
                'cart_items': cart_items,
                'grand_total': grandtotal,
                'discount': Discount,
                'total_with_original_price': total_with_original_price,
                'wallet': wallet.balance

            }

            return render(request, 'user_templates/payment.html', context)
        
        return render (request,'user_templates/home.html')

    def post(self, request): 
        data = json.loads(request.body)
        selected_option = data.get('payment_option')
        
        if selected_option == 'option3':
           
            url='/order-place-cod/'

        elif selected_option == 'option1':
            user_id = request.user.id

            # Get necessary instances
            
            payment_methods_instance = PaymentMethod.objects.get(method_name="RAZORPAY")
            user_instance = Account.objects.get(id=user_id)
            try:
                address = AdressBook.objects.get(is_default=True, user=user_instance)
            except AdressBook.DoesNotExist:
                address = None
                messages.error(request, 'address not added')

            cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
            
            if cart_items.count()>=1:

                total_with_original_price = 0
                total = 0
                quantity = 0

                for cart_item in cart_items:
                    total += cart_item.sub_total()
                    total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
                    quantity += cart_item.quantity

                Discount = request.session.get('discount', Decimal('0')) 
                total_float = float(total)
                Discount_float = float(Discount)

                grand_total = total_float - Discount_float
                address = AdressBook.objects.get(is_default=True, user=user_instance)

                
                address1 =[address.name,
                        address.address_line_1,
                        address.locality,
                        address.city,
                        address.state,
                        address.country,
                        address.pincode,
                        address.phone
                        ]
              
                for cart_item in cart_items:
                    product = cart_item.product
                    product.stock -= cart_item.quantity
                    product.save()
            

                # Create ShippingAddress instance
                
                print('=========================')

                client = razorpay.Client(auth=("rzp_test_vAeyohaspEahRA", "076FQiZmu52B1ODs1UWKe2HF"))
                data = { "amount":(int(grand_total)*100), "currency": "INR" }
                payment1 = client.order.create(data=data)
                print(payment1)
                payment_order_id = payment1['id']
                print(payment_order_id)

                payment = Payment.objects.create(user=user_instance,
                                            payment_method=payment_methods_instance,
                                            amount_paid=grand_total,
                                            payment_status='PENDING',
                                            payment_order_id=payment_order_id
                                            )  
                 
                draft_order= Order.objects.create(
                    user=user_instance,
                    shipping_address=address1,
                    order_total=grand_total,
                    is_ordered  = True,
                    payment = payment,
                    additional_discount=Discount_float,
                    grand_total=total_float
                )

                for cart_item in cart_items:
                        
                        OrderProduct.objects.create(
                            order           = draft_order,
                            user            = user_instance,
                            product_variant = cart_item.product.get_product_name(),
                            product_id      = cart_item.product.id,
                            quantity        = cart_item.quantity,
                            product_price   = float(cart_item.product.sale_price),
                            images          = cart_item.product.thumbnail_image,
                            ordered         = True,
                        )     
                cart_items.delete() 

                return JsonResponse({'message': 'Success', 'context': payment1})      
        else:
            print('selected')
            url='/order-place-wallet/'

        return JsonResponse({'success': False, 'message': 'Error processing request','url':url})



def order_place_cod(request):

    user_id = request.user.id

    payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")

    user_instance = Account.objects.get(id=user_id)

    try:
        address = AdressBook.objects.get(is_default=True, user=user_instance)
    except AdressBook.DoesNotExist:
        address = None
        messages.error(request, 'address not added')

    cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
    
   

    total_with_original_price = 0
    total = 0
    quantity = 0

    for cart_item in cart_items:
        total += cart_item.sub_total()
        total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
        quantity += cart_item.quantity
    Discount = request.session.get('discount', Decimal('0')) 
    total_float = float(total)
    Discount_float = float(Discount)

    grand_total = total_float - Discount_float
    
    if grand_total <= 100000:
    # Create ShippingAddress instance
        address1 =[address.name,address.address_line_1,address.locality,address.city,address.state,address.country,address.pincode,address.phone]

        payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=0,payment_status='SUCCESS')
        
        
        draft_order= Order.objects.create(
                        user=user_instance,
                        shipping_address=address1,
                        order_total=grand_total,
                        is_ordered  = True,
                        payment = payment,
                        additional_discount=Discount_float,
                        grand_total=total_float

                    )
        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
            
        for cart_item in cart_items:
                OrderProduct.objects.create(
                    order           = draft_order,
                    user            = user_instance,
                    product_variant = cart_item.product.get_product_name(),
                    product_id      = cart_item.product.id,
                    quantity        = cart_item.quantity,
                    product_price   = float(cart_item.product.sale_price),
                    images          = cart_item.product.thumbnail_image,
                    ordered         = True,
                )
                cart_id=Cart.objects.get(id=cart_item.cart.id)
                print(cart_id)
        cart_id.delete() 

        cart_items.delete()    
    
        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order) 

        for i in order_dtails:
            address=i.order.shipping_address
    else:
        messages.error(request, 'COD not available of order above 100000 ,choose another option')
        return redirect('order-payment')

        


    cleaned_string = address.replace('[', '').replace(']', '')

    # Split the string by comma and remove empty strings and 'None' values
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]
    
    context = {
                'order_dtails' : draft_order,
                'order_product' : order_dtails,
                }

    return render (request,'user_templates/order_sucess.html',context)

def order_place_Wallet(request):

    user = request.user.id
    user_instance = Account.objects.get(id=user)
    wallet=Wallet.objects.get(user=user_instance)

    payment_methods_instance = PaymentMethod.objects.get(method_name="WALLET")

    
    try:
        address = AdressBook.objects.get(is_default=True, user=user_instance)
    except AdressBook.DoesNotExist:
        address = None
        messages.error(request, 'address not added')

    cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
  
    total_with_original_price = 0
    total = 0
    quantity = 0


    for cart_item in cart_items:
        total += cart_item.sub_total()
        total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
        quantity += cart_item.quantity
    Discount = request.session.get('discount', Decimal('0')) 
    total_float = float(total)
    Discount_float = float(Discount)

    grand_total = total_float - Discount_float

    if wallet.balance >=grand_total:
    
        wallet.balance -= grand_total
        wallet.save()
        WalletTransaction.objects.create(wallet=wallet, amount=grand_total, transaction_type='DEBIT')


        # Create ShippingAddress instance
        
        print('==================....=======')

        payment = Payment.objects.create(user=user_instance,
                                    payment_method=payment_methods_instance,
                                    amount_paid=grand_total,
                                    payment_status='SUCESS',
                                    
                                    )   


        # Create ShippingAddress instance
        address1 =[address.name,address.address_line_1,address.locality,address.city,address.state,address.country,address.pincode,address.phone]
          
        draft_order= Order.objects.create(
                        user=user_instance,
                        shipping_address=address1,
                        order_total=grand_total,
                        is_ordered  = True,
                        payment = payment,
                        additional_discount=Discount_float,
                        grand_total=total_float
                    )
        
        for cart_item in cart_items:
            product= cart_item.product
            product.stock -= cart_item.quantity
            product.save()
            
        for cart_item in cart_items:
                OrderProduct.objects.create(
                    order           = draft_order,
                    user            = user_instance,
                    product_variant = cart_item.product.get_product_name(),
                    product_id      = cart_item.product.id,
                    quantity        = cart_item.quantity,
                    product_price   = float(cart_item.product.sale_price),
                    images          = cart_item.product.thumbnail_image,
                    ordered         = True,
                )

                cart_id=Cart.objects.get(id=cart_item.cart.id)
                print(cart_id)
        cart_id.delete() 

        cart_items.delete()    
       
        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order) 



        for i in order_dtails:
            address=i.order.shipping_address
        
    else:
       
        messages.error(request, 'NO ENOUGH BALANCE ,choose another option')
        return redirect('order-payment')
        

    cleaned_string = address.replace('[', '').replace(']', '')

    # Split the string by comma and remove empty strings and 'None' values
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]
    

    context = {
                'order_dtails' : draft_order,
                'address' : cleaned_data,
                'order_product' : order_dtails,
                }

    return render (request,'user_templates/order_sucess.html',context)


@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":

        try:
            # Extract payment details from the POST request
            payment_id        = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature         = request.POST.get('razorpay_signature', '')
            print(f'1:{payment_id},2:{razorpay_order_id},3:{signature}')
            # Create a dictionary of payment parameters
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            }

            # Verify the payment signature
            client = razorpay.Client(auth=('rzp_test_vAeyohaspEahRA', '076FQiZmu52B1ODs1UWKe2HF'))
            result = client.utility.verify_payment_signature(params_dict)

            if not result :
                return redirect('payment_failure')

            else:
              
                payment = Payment.objects.get(payment_order_id=razorpay_order_id)
                payment.payment_status = 'SUCCESS'
                payment.payment_id = payment_id
                payment.save()

                user_instance = payment.user

                address = AdressBook.objects.get(is_default=True, user=user_instance)
                draft_order= Order.objects.get(payment=payment)
                order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order) 

                print(draft_order,'gggg')
                for i in order_dtails:
                    address=i.order.shipping_address

                cleaned_string = address.replace('[', '').replace(']', '')

                    # Split the string by comma and remove empty strings and 'None' values
                split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

                # Remove single quotes from each item
                cleaned_data = [item.replace("'", "") for item in split_data]
                

                context = {
                            'order_dtails' : draft_order,
                            'address' : cleaned_data,
                            'order_product' : order_dtails,
                            }

                return redirect('success_page', draft_order.id)
               
        except Exception as e:
            # Exception occurred during payment handling
            print('Exception:', str(e))
            return redirect('payment_failure')
    else:
        return redirect('payment')
    

def payment_failure(request):

    order=Order.objects.all().order_by('-created_at').first()
    return render(request, 'user_templates/failure_page.html',{"order":order})    
    

def success_page(request, id):

    draft_order= Order.objects.get(id = id)
    order_dtails=OrderProduct.objects.filter(order=draft_order) 

    print(draft_order,'gggg')
    for i in order_dtails:
        address=i.order.shipping_address

    cleaned_string = address.replace('[', '').replace(']', '')

    # Split the string by comma and remove empty strings and 'None' values
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]
               
    context={
        'order_dtails' : draft_order,
        'address' : cleaned_data,
        'order_product' : order_dtails,
    }
    return render (request,'user_templates/order_sucess.html',context)


def get_current_step(request):

    d_id = request.GET.get('d_id')
    order_dtails=OrderProduct.objects.get(id=d_id)
    print('getttt',order_dtails.order_status)
    if order_dtails.order_status=='New':
        current_step = 1
    elif order_dtails.order_status=='Accepted':
        current_step = 2 
    elif order_dtails.order_status=='Shipped':
        current_step = 3  
    elif order_dtails.order_status=='Delivered':
        current_step = 4  

    print(current_step)

    return JsonResponse({'currentStep': current_step})


def orders_return(request):

    user_id = request.user.id

    user_instance = Account.objects.get(id=user_id)

    if request.method == 'POST':
        data = json.loads(request.body)
        orderId = data.get('orderId')
        returnReason = data.get('returnReason')

        order_dtails=OrderProduct.objects.get(id=orderId,user=user_instance)
        order_dtails.order_status='Return Status'
        order_dtails.save()
        
        return_request=ReturnRequest(
            order_product=order_dtails,
            user=user_instance,
            reason=returnReason,
        )
        return_request.save()


        return JsonResponse({'status': 'success', 'orderId': orderId, 'returnReason': returnReason})
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)