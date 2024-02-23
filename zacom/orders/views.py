from decimal import Decimal
from django.shortcuts import render,redirect
from django.urls import reverse
from customers.models import Account,AdressBook
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from cart.models import CartItem,Cart
from products.models import Product_Variant
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from .models import Payment,PaymentMethod,OrderProduct,Order

@method_decorator(login_required, name='dispatch')
class Review(View):
    
    def get(self,request):
        
    # if the cart count is less than or equal to 0 ,then redirect back to shop
        
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        cart_count = cart_items.count()
        if cart_count < 0:
            return redirect('shop')
        
        for i in cart_items:
            pass
        

        total_with_orginal_price =0
        total=0
        quantity=0

        try:
        
                cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    
                print(cart_items)
                for cart_item in cart_items:
                    total += cart_item.sub_total()
                    # total += ( cart_item.product.sale_price * cart_item.quantity)
                    total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
                    quantity += cart_item.quantity
                    
            
                
        except ObjectDoesNotExist:
            pass
        
        discount = total_with_orginal_price - total
        grand_total = total
       

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'grand_total':grand_total,
            'discount':discount,
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

            discount = total_with_orginal_price - total
            grand_total = total
            


            context = {'adress': address,
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'grand_total':grand_total,
            'discount':discount,
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
        cart_items = CartItem.objects.filter(user=user, is_active=True)

        total_with_original_price = 0
        total = 0
        quantity = 0

        for cart_item in cart_items:
            total += cart_item.sub_total()
            total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity

        discount = total_with_original_price - total
        grand_total = total

        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'grand_total': grand_total,
            'discount': discount,
            'total_with_original_price': total_with_original_price
        }

        return render(request, 'user_templates/payment.html', context)

    def post(self, request): 
        data = json.loads(request.body)
        selected_option = data.get('payment_option')
        
        if selected_option == 'option3':
            print('selected')
            url='/order-place/'
        else:
            print('review')
            url='/order-review/'
        return JsonResponse({'success': False, 'message': 'Error processing request','url':url})


def order_place(request):

    user_id = request.user.id

    # Get necessary instances
    
    payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")

    user_instance = Account.objects.get(id=user_id)

    address = AdressBook.objects.get(is_default=True, user=user_instance)

    cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
    
    if cart_items.count()>=1:



        total_with_original_price = 0
        total = 0
        quantity = 0

        for cart_item in cart_items:
            total += cart_item.sub_total()
            total_with_original_price += (cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total = total

        # Create ShippingAddress instance
        address1 =[address.name,address.address_line_1,address.locality,address.city,address.state,address.country,address.pincode,address.phone]
        
        

        # Create Payment instance
        payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=0,payment_status='PENDING')
        
        
        draft_order= Order.objects.create(
                user=user_instance,
                shipping_address=address1,
                order_total=grand_total,
                is_ordered  = True,
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
                    quantity        = cart_item.quantity,
                    product_price   = float(cart_item.product.sale_price),
                    images          = cart_item.product.thumbnail_image,
                    ordered         = True,
                )

        cart_items.delete()    
       
        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
        for i in order_dtails:
            address=i.order.shipping_address
        
    else:

        draft_order=Order.objects.filter(user=user_instance).order_by('-created_at').first()
        order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
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
                'order_product' : order_dtails
                }

   

    return render (request,'user_templates/order_sucess.html',context)

def get_current_step(request):

    d_id = request.GET.get('d_id')
    order_dtails=Order.objects.get(id=d_id)
 
    if order_dtails.order_status=='New':
        current_step = 1
    elif order_dtails.order_status=='Accepted':
        current_step = 2  # Example: You can fetch this from the database or any other source
    elif order_dtails.order_status=='Delivered':
        current_step = 4  # Example: You can fetch this from the database or any other source
    else :
        current_step = 2  # Example: You can fetch this from the database or any other source
  
    # Return the current step as JSON response
    return JsonResponse({'currentStep': current_step})


def orders_return(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        orderId = data.get('orderId')
        returnReason = data.get('returnReason')

        print(orderId,returnReason)
        # Process orderId and returnReason as needed
        return JsonResponse({'status': 'success', 'orderId': orderId, 'returnReason': returnReason})
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)