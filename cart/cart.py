from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # if the user is new, we should create new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages of site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            print('current_user in add', current_user)
            # Convert {'3': 1} to {"3": 1}
            carty = str(self.cart)
            print('carty', carty)
            carty = carty.replace('\'', '\"')
            # Save our carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        # Get the ids
        product_ids = self.cart.keys()
        # lookup those keys in Product DB model
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            value_int = int(value)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value_int)
                    else:
                        total = total + (product.price * value_int)

        return total

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        # Get Ids from cart
        product_ids = self.cart.keys()
        print('product_ids', product_ids)
        # use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantities(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = quantity
        print(' in def update ', product_qty)
        # Get Cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        some = self.cart
        return some

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


