from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import CartItem,Cart
from products.models import Product_Variant
from django.http import JsonResponse
from orders.models import Payment
from django.contrib import messages

# Create your views here.
#to get the cart id if present
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def cart(request,total=0,quantity=0,cart_items=None):
    total_with_orginal_price =0

    try:

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
          


        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
           
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
        'total_with_orginal_price':total_with_orginal_price,
    }

    if total==0:
      return render(request, 'user_templates/shop_cart_empty.html',context)

    else:
      
      return render(request, 'user_templates/shop-cart.html',context)

 

def add_cart(request,product_id):
    current_user = request.user
    product = Product_Variant.objects.get(id=product_id)    #get the product
    
    if request.GET.get('quantity'):
        quantity1 = int(request.GET.get('quantity'))
        print(quantity1)
    else:
        quantity1=1
       
    #if user authenticated
    if current_user.is_authenticated:

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cartid present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        


        try:
            cart_item = CartItem.objects.get(product=product , user=current_user)
            print('1stttttttttttttttttttttt')
            maxstock=cart_item.quantity + quantity1
            if maxstock <= product.stock:
                cart_item.quantity += quantity1
                cart_item.save()
            else:
                messages.error(request, 'Stock limit exceed')
    

        except CartItem.DoesNotExist:
            print('12stttttttttttttttttttttt')

            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                cart=cart,
                quantity = quantity1,
            )
            cart_item.save()
        return redirect('cart')
        
    else:
        
        # ===CART CREATED ===
        try:
            print('3stttttttttttttttttttttt')

            cart = Cart.objects.get(cart_id=_cart_id(request)) # to get the cartid present in the session
        except Cart.DoesNotExist:
            print('13stttttttttttttttttttttt')

            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        
        # ===Product saved to cart item
        try:
            print('assstttttttttttttttttttttt')

            cart_item = CartItem.objects.get(product=product , cart=cart)
            maxstock=cart_item.quantity + quantity1
            if maxstock <= product.stock:
                cart_item.quantity += quantity1
                cart_item.save()
            else:
                messages.error(request, 'Stock limit exceed')

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity = quantity1,
            )
            cart_item.save()
        return redirect('cart')

def update_cart(request, cart_item_id, new_quantity):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity = int(new_quantity)
        cart_item.save()
        print(cart_item)
        print(cart_item)
        
        
        response_data = {
            'success': True,
            'message': 'Cart updated successfully',
            'subtotal': cart_item.sub_total(),
            'grand_total':11
        }

    except CartItem.DoesNotExist:
        response_data = {
            'success': False,
            'message': 'Cart item not found',
        }

    return JsonResponse(response_data)


def delete_cart_item(request, cart_item_id):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(id=cart_item_id,user=request.user,is_active=True)


    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True,id=cart_item_id)

    cart_items.delete()
    print('aaaaa')
    response_data = {
        'success': True,
        'message': 'Item deleted successfully',
    }

   
      

    return JsonResponse(response_data)




def order_summary(request):
    # Your existing code to calculate order summary
    total = 0
    quantity = 0
    shipping = 100

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)

    # Calculate total, quantity, tax, and grandtotal
    for cart_item in cart_items :
        total += round(cart_item.sub_total(), 2)
        quantity += cart_item.quantity

    tax = round(total / 100 * 5, 2)
    grandtotal = round(tax + total + shipping, 2)
    Discount =grandtotal-total
    # Return JSON response
    return JsonResponse({
        'total': total,
        'quantity': quantity,
        'shipping': shipping,
        'tax': tax,
        'grandtotal': grandtotal,
        'Discount':Discount
    })



