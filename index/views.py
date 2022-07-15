from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import *
from .forms import SearchForm, RegisterUserForm

# TgBot Connection
from .handlers import bot



def main_page(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    # Форма для поиска
    search_bar = SearchForm()

    context = {
        'products': all_products,
        'categories': all_categories,
        'form': search_bar
    }

    if request.method == 'POST':
        product_to_find = request.POST.get('search_product')

        try:
            search_result = Product.objects.get(product_name=product_to_find)

            return redirect(f'{search_result.id}/')

        except:
            return redirect('/')
    return render(request, 'index/index.html', context)


def get_full_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        Cart.objects.create(user_id=request.user.id,
                            user_product=product,
                            user_product_quantity=request.POST.get('product_quantity'))
        return redirect('/')

    context = {
        'product': product
    }
    return render(request, 'index/about_product.html', context)


def get_full_category(request, pk):
    all_products = Product.objects.filter(product_category=pk)
    context = {
        'products': all_products
    }

    return render(request, 'index/categrory_products.html', context)


def get_user_cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        main_text = 'Новый заказ\n\n'

        for i in user_cart:
            main_text += f'Товар {i.user_product} Количество: {i.user_product_quantity}\n'

        bot.send_message(275755142, main_text)
        user_cart.delete()
        return redirect('/')

    return render(request, 'index/user_cart.html', {'cart': user_cart})


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


def delete_item_from_cart(request, pk):
    user_cart = Cart.objects.filter(user_id = request.user.id, user_product=pk)
    user_cart.delete()

    return redirect('/cart')


# def register(request):
#     form = RegisterUserForm
#     # print(request)
#     if request.method == 'POST':
#         User.objects.create_user(username=request.POST.get('username'),
#                             password=request.POST.get('password'))
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'registration/register.html', context)


def about(request):
    return HttpResponse('About us')


def contacts(request):
    return HttpResponse('Contacts')


def content(request, ):
    return HttpResponse('content')
