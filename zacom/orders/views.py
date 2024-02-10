from django.shortcuts import render
from customers.models import Account,AdressBook
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from cart.models import CartItem,Cart
from products.models import Product_Variant
from django.http import JsonResponse



# Create your views here.
@login_required(login_url='login')
def address(request):
    user = request.user.id
    address = AdressBook.objects.filter(user=user)
   
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_address_id = data.get('addressId')

        # print(selected_address_id)
        if selected_address_id:
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

    context = {'adress': address}
    print('xxx',user,address)

    return render (request,'user_templates/checkout.html',context)

def review(request):
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
    print( 'total',total,
        'quantity',quantity,
        'cart_items',cart_items,
        'grand_total',grand_total,
        'discount',discount,
        'total_with_orginal_price',total_with_orginal_price)
    return render (request,'user_templates/order_summary.html',context)

def payment(request):
    return render (request,'user_templates/payment.html')

