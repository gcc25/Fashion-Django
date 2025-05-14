from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    size=item.get('size'),
                    color=item.get('color')
                )
            
            # Clear the cart
            cart.clear()
            messages.success(request, "Your order has been placed successfully!")
            return render(request, 'orders/order_created.html', {'order': order})
    else:
        # Pre-fill form with user details
        user_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        # Get previous order details if they exist
        previous_order = Order.objects.filter(user=request.user).order_by('-created').first()
        if previous_order:
            user_data.update({
                'address': previous_order.address,
                'postal_code': previous_order.postal_code,
                'city': previous_order.city,
                'country': previous_order.country,
                'phone': previous_order.phone,
            })
        form = OrderCreateForm(initial=user_data)
    
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})