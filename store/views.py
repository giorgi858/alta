from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

def home_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html',  context)


def category_summary(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'category_summary.html',  context)


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Password Has Been Successfully Updated!!')
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            context = {
                'form': form
            }
            return render(request, 'update_password.html',  context)
    else:
        messages.success(request, 'You must be logged in to view that page..')
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        print("current_user", current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'User Has Been Updated!!')
            return redirect('home')
        else:
            context = {
                'user_form': user_form
            }
            return render(request, 'update_user.html', context)

    else:
        messages.success(request, 'You Must Been Logged In To Access This Page!!')
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        print("current_user", current_user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your Info Has Been Updated')
            return redirect('home')
        else:
            context = {
                'form': form
            }
            return render(request, 'update_info.html', context)

    else:
        messages.success(request, 'You Must Been Logged In To Access This Page!!')
        return redirect('home')


def about(request):
    context = {}
    return render(request, 'about.html', context)


def category(request, foo):
    foo = foo.replace('!', "'")
    # წამომიღე კატეგორია მოდელიდან ისეთი
    # ფილდი რომესაც name ჰქვია და თუ ეს ფილდი ტოლია foo-სი და
    # ეს foo არის ის რაც category/<str:foo> აქ იქნება foo. category/
    # და მერე კონკრეტული კატეგორიის სახელი
    specific_category = Category.objects.get(name=foo)
    products = Product.objects.filter(category=specific_category)
    context = {
        'products': products,
        'specific_category': specific_category
    }
    return render(request, 'category.html', context)


def login_user(request):
    if request.method == 'POST':
        login_username = request.POST['username']
        login_password = request.POST['password']
        user = authenticate(request, username=login_username, password=login_password)
        if user is not None:
            login(request, user)
            messages.success(request, ' Successfully Login, Congratulation')
            return redirect('home')
        else:
            messages.success(request, 'error message')
            return redirect('login')
    else:
        context = {}
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'successfully logout')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created - Please Fill Out Your User Info Bellow...")
            return redirect('update_info')
        else:
            messages.success(request, 'error register')
            return redirect('register')
    else:
        context = {
            'form': form
        }
        return render(request, 'register.html', context)


def product(request, foo):
    product = Product.objects.get(id=foo)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        # Query The Product DB model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        print('searched', searched)
        # Test for null
        if not searched:
            messages.success(request, 'That Product Does Not Exist... Please try again')
            return render(request, 'search.html', {})
        else:
            context = {
                'searched': searched
            }
            return render(request, 'search.html', context)
    else:
        context = {}
        return render(request, 'search.html', context)


