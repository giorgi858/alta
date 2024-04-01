from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product, Category
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # Get cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities()
    print('cart_products f', cart_products)
    total = cart.cart_total()
    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'total': total,
    }
    return render(request, 'cart_summary.html', context)


def cart_add(request):
    # Get Cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = request.POST.get('product_qty')
        print("product_qty in view.py", product_qty)
        print('product_id', product_id)

        # Lookup Product in DB
        product = get_object_or_404(Product, id=product_id)
        print('product', product)

        # Save To Session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()
        print('cart len', cart_quantity)

        # Return response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ' Product Added To Cart')
        return response


def cart_delete(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        # call delete Func in Cart
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request, ' Product Removed To Cart')

        return response


def cart_update(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        print('product_qty in view.py', product_qty)
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request, ' Product Updated')

        return response






