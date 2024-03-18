from .models import CartItem,Wishlist,Cart
from .views import _cart_id 



def wishlist_count(request):
    current_user = request.user
    count = 0
    if current_user.is_authenticated:  # Corrected typo: is_authenticated
        try:
            wishlist_instance = Wishlist.objects.get(user=current_user)
            products = wishlist_instance.product.all()
            count = products.count()
        except Wishlist.DoesNotExist:
            pass
    return {'wishlist_count': count}

def cart_count(request):
    current_user = request.user
    count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        count=cart_items.count()
    else:
        try:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_items = CartItem.objects.filter(cart=cart, is_active=True)
           count=cart_items.count() 
        except Cart.DoesNotExist:  
            pass
          
    return {'cart_count': count}