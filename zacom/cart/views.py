from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from .models import CartItem,Cart,Wishlist
from products.models import Product_Variant
from django.http import JsonResponse
from orders.models import Payment
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from products.models import Coupon,UserCoupon
import json
from django.utils import timezone
from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# Create your views here.
#to get the cart id if present
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@never_cache 
def cart(request,total=0,quantity=0,cart_items=None):
    
    total_with_orginal_price =0
     
    discount = total_with_orginal_price - total
    grand_total = total
    request.session['grandtotal'] = str(grand_total)

    limit=0
   
    coupon_detail=None

    try:

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            cart = None  # Initialize cart outside of the try block
            for i in cart_items:
                cart = i.cart

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        coupon_detail = None  # Initialize coupon_detail outside of the try block
        if cart and cart.coupon and cart.coupon.coupon:
            # Retrieve the coupon instance based on the coupon code
            coupo = Coupon.objects.get(coupon_code=cart.coupon.coupon)
            if not coupo.is_expired and coupo.total_coupons > 0:
                # Check if the coupon is valid and has remaining uses
                coupon_detail = coupo
            else:
                # Handle cases where the coupon is expired or has no remaining uses
                messages.error(request, "Coupon is expired or not valid")
        else:
            pass

        for cart_item in cart_items:
            total += cart_item.sub_total()
            offer=cart_item.product.apply_offer_discount()
            print('offer',offer)
            total_with_orginal_price +=( cart_item.product.max_price * cart_item.quantity)
            quantity += cart_item.quantity
            print('ss',offer)
            if cart_item.quantity > cart_item.product.stock:
                    limit=1
                    messages.error(request, f"Insufficient stock for {cart_item.product}")

                    return render(request, 'user_templates/shop-cart.html', {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'grand_total': grand_total,
                    'discount': discount,
                    'total_with_orginal_price': total_with_orginal_price,
                    'limit' : limit,
                    'cart':cart.id,
                    'coupon_detail':coupon_detail,
                })
           
        
  
    except ObjectDoesNotExist:
        pass
   
     
    if total_with_orginal_price == 0:
      
        if 'discount' in request.session:
            del request.session['discount']
        return render(request, 'user_templates/shop_cart_empty.html')
    
    else:

        return render(request, 'user_templates/shop-cart.html', {
                    'total': total,
                    'quantity': quantity,
                    'cart_items': cart_items,
                    'grand_total': grand_total,
                    'discount': discount,
                    'total_with_orginal_price' : total_with_orginal_price,
                    'limit' : limit,
                    'coupon_detail': coupon_detail,
                    'cart':cart.id,
                })

 

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
            cart_item = CartItem.objects.get(product=product,user=current_user)
            print('1stttttttttttttttttttttt')
            maxstock=cart_item.quantity + quantity1
            if maxstock <= product.stock:
                cart_item.quantity += quantity1
                cart_item.save()
                messages.error(request, 'Product Added')
            else:
                messages.error(request, 'Stock limit exceed')
    

        except CartItem.DoesNotExist:
            print('12stttttttttttttttttttttt')
            if quantity1 <= product.stock:
                cart_item = CartItem.objects.create(
                    product=product,
                    user=current_user,
                    cart=cart,
                    quantity = quantity1,
                )
                cart_item.save()
                messages.error(request, 'Product Added')
            else:
                messages.error(request, 'Stock limit exceed')

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
            print(cart)
            
        # ===Product saved to cart item
        try:
            print('assstttttttttttttttttttttt')

            cart_item = CartItem.objects.get(product=product,cart=cart)
            maxstock=cart_item.quantity + quantity1
            if maxstock <= product.stock:
                cart_item.quantity += quantity1
                cart_item.save()
                messages.error(request, 'Product Added')

            else:
                messages.error(request, 'Stock limit exceed')

        except CartItem.DoesNotExist:
            if quantity1 <= product.stock:
                cart_item = CartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity = quantity1,
                )
                cart_item.save()
                messages.error(request, 'Product Added')
            else:
                messages.error(request, 'Stock limit exceed')
    # return redirect(reverse('product_detail', kwargs={'product_variant_slug': product.product_variant_slug}))
    return redirect(request.META.get('HTTP_REFERER', '/'))

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

@never_cache 
def order_summary(request):
    # Your existing code to calculate order summary
    total = Decimal(0) 
    quantity = Decimal(0) 
    shipping = Decimal(100) 

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)

    # Calculate total, quantity, tax, and grandtotal
    for cart_item in cart_items :
        total += round(cart_item.sub_total(), 2)
        quantity += cart_item.quantity
        cart_id = cart_item.cart.id

    tax = round(total / 100 * 5, 2)
    grandtotal = round( total , 2)
    request.session['grandtotal'] = float(grandtotal)
    grand_total_session = request.session['grandtotal'] 

    Discount = request.session.get('discount')
    if Discount is None:
        Discount = 0  
        request.session['discount'] = Discount

    grandtotal = grand_total_session - Discount    

    return JsonResponse({
        'total': total,
        'quantity': quantity,
        'shipping': shipping,
        'tax': tax,
        'grandtotal': grandtotal,
        'Discount':Discount,
        'cart_id': cart_id,
    })


def apply_coupon(request):

    if request.method == 'POST':
        discount_amount = 0 
        if 'discount' in request.session:
            del request.session['discount']
            print(discount_amount,'ddiscount')

        if discount_amount == 0 :
            data = json.loads(request.body)
            coupon_code = data.get('coupon')
            coupn_dict = {'coupon':coupon_code,}
            cache.set('coupon_code',coupn_dict )
            print(coupon_code)
            grand_total = float(request.session.get('grandtotal'))
            print('grandd',grand_total)
        
            try:
                # Attempt to get the Coupon object based on the provided coupon code
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                print(coupon,'1')
            except Coupon.DoesNotExist:
                # Handle the case where the coupon does not exist
                data = {'error': 'Coupon does not exist'}
                return JsonResponse(data, status=200)
            
            try:
                # Attempt to get the UserCoupon object for the current user and coupon
                cart_item_instance= CartItem.objects.filter(user=request.user)
                for i in cart_item_instance:
                    i.cart.id
                cart_instance = Cart.objects.get(id=i.cart.id)   
                coupon_usage, created = UserCoupon.objects.get_or_create(
                coupon=coupon,
                user=request.user,
                defaults={'usage_count': 0}  # Set default values for newly created instance
                ) 

                cart_instance.coupon = coupon_usage
                cart_instance.save()
                print('sucess',cart_instance)
                print(coupon_usage.id, '2')
            except UserCoupon.DoesNotExist:
                # Handle the case where the UserCoupon does not exist
                data = {'error': 'UserCoupon does not exist'}
                return JsonResponse(data, status=200)
            
            discount=coupon.discount
            if coupon_usage.apply_coupon() and grand_total >= float(coupon.minimum_amount):
                discount_amount = grand_total-discount
                coupon.total_coupons -= 1
                coupon.save()
                print(discount_amount, 'Success')
                request.session['discount'] = round(discount,2) 
                print('grandd',grand_total)
                data={'discount_amount':discount_amount,'discount':discount}
                print(data,'3')
                return JsonResponse({'success':'Coupon Applied'})
                
            else:

                if coupon.expire_date < timezone.now().date():
                    data={'error':'Coupon expired'}
                    print('Failed')
                    return JsonResponse(data)
                elif grand_total < float(coupon.minimum_amount):
                    data={'error':'Minimum amount required'}
                    print('Failed')
                    return JsonResponse(data)
                elif coupon.total_coupons == 0:
                    data={'error':'Coupon not available'}
                    print('Failed')
                    return JsonResponse(data)
                data={'error':'Maximum uses of the coupon reached'}
                print('Failed')
                return JsonResponse(data)
            
        else:
            return JsonResponse({'error': 'Coupon already applied'})
        

def delete_applied_coupon(request,cart_item_id):
    print('xx1',cart_item_id)
    if 'discount' in request.session:
        del request.session['discount']
        
    if request.user.is_authenticated:
        cart = Cart.objects.get(id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True,id=cart_item_id)
   
    try:
        if cart.coupon:  # Check if cart has a coupon applied
            coupon_detail = UserCoupon.objects.get(id=cart.coupon.id)
            coupon_detail.usage_count -= 1
            coupon_detail.save()

            cart.coupon=None
            cart.save()


    except UserCoupon.DoesNotExist:
        pass

    if 'discount' in request.session:
        del request.session['discount']
        print('del  discount')
    print('aaaaapd')

    response_data = {
        'success': True,
        'message': 'coupon deleted successfully',
    }

    return JsonResponse(response_data)

@login_required(login_url='login')
@never_cache 
def wishlist(request):
    current_user = request.user
    try:
        wishlist_instance= Wishlist.objects.get(user=current_user)
    except Wishlist.DoesNotExist:
        wishlist_instance = Wishlist.objects.create(user=current_user)
        
    products = wishlist_instance.product.all()
    count=products.count()
    
    context={
        'wishlist' : products,
        'count':count

    }
    return render(request, 'user_templates/wishlist.html',context)

@login_required(login_url='login')
def wishlist_add(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product_Variant, id=product_id) 
    
    try:
        # Get or create the Wishlist object for the current user
        wishlist_instance, created = Wishlist.objects.get_or_create(user=current_user)
        
        # Check if the product is already in the wishlist
        if product in wishlist_instance.product.all():
            messages.error(request, 'Product already exists in your wishlist.')
        else:
            wishlist_instance.product.add(product)
            messages.success(request, 'Product added to your wishlist.')

    except Wishlist.DoesNotExist:
        # Create a new Wishlist object for the current user
        wishlist_instance = Wishlist.objects.create(user=current_user)
        wishlist_instance.product.add(product)
        messages.success(request, 'Product added to your wishlist.')

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
def wishlist_remove(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product_Variant, id=product_id) 
    
    try:
     
        wishlist_instance= Wishlist.objects.get(user=current_user)
        wishlist_instance.product.remove(product)
        messages.success(request, 'Product removed from your wishlist.')

    except Wishlist.DoesNotExist:
        pass
        
    return redirect('wishlist')