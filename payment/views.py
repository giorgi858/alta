from django.shortcuts import render
from cart.cart import Cart


def payment_success(request):
    context = {}
    return render(request, 'payment/payment_success.html', context)


def checkout(request):
    # Get cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities()
    print('quantities', quantities)
    total = cart.cart_total()
    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'total': total,
    }
    return render(request, 'payment/checkout.html', context)
