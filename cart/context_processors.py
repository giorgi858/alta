from .cart import Cart


# Create context processor so our cart works on all pages of the site
def cart(request):
    # Return default data from Cart
    return {'cart': Cart(request)}
