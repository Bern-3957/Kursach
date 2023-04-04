import random

from django.contrib.auth import logout, login
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from .models import *
from .forms import *
from django.db.models import Count
# import pandas as pd
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormView
from .helpers import get_good
from django.contrib.auth.decorators import login_required

# Create your views here.
menu = [{'title': 'Услуги', 'url_name': 'services'},
        {'title': 'Каталог продукции', 'url_name': 'shop_catalog'},
        {'title': 'О компании', 'url_name': 'about_us'},
        {'title': 'Контакты', 'url_name': 'contacts_ways'},
        ]
memory = {
    'good_id_to_basket': [],
    'basket_total_price': 0
}
select_items = [
    {'number': '0', 'title': 'По умолчанию', 'order': 'ordinary_price'},
    {'number': '1', 'title': 'По возр. цены', 'order': 'price'},
    {'number': '2', 'title': 'По убыв. цены', 'order': '-price'},

]


class IndexListView(ListView):
    model = Products
    context_object_name = 'products'
    template_name = 'UralsSteelStore/index.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        form = ModalRequestForm()
        self.object_list = self.get_context(form=form)
        return render(request, self.template_name, context=self.object_list)

    def post(self, request, *args, **kwargs):
        form = ModalRequestForm(request.POST)
        context = self.get_context(form=form)
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, self.template_name, context=context)

    def get_context(self, **kwargs):
        context = dict()
        category_id = 1
        context['menu'] = menu
        context['category_id'] = self.kwargs['category_id'] if 'category_id' in self.kwargs else category_id
        if 'form' in kwargs:
            context['form'] = kwargs['form']

        return context


class ServicesView(View):
    template_name = 'UralsSteelStore/services.html'

    def get(self, request, *args, **kwargs):
        form = ModalRequestForm()
        context = {}

        context['form'] = form
        context['menu'] = menu
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = ModalRequestForm(request.POST)
        context = {}
        if form.is_valid():
            print(form.cleaned_data)

        context['form'] = form
        context['menu'] = menu
        return render(request, self.template_name, context=context)


class Metal_cutting_View(View):
    template_name = 'UralsSteelStore/metal_cutting.html'

    def get(self, request, *args, **kwargs):
        form = RequestForm()
        context = {}
        context['form'] = form
        context['menu'] = menu
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = RequestForm(request.POST)
        context = {}
        if form.is_valid():
            print(form.cleaned_data)

        context['form'] = form
        context['menu'] = menu
        return render(request, self.template_name, context=context)


def shop_catalog(request, slug_cat=None, ):
    select_items = [
        {'number': '0', 'title': 'По умолчанию', 'order': 'ordinary_price'},
        {'number': '1', 'title': 'По возр. цены', 'order': 'price'},
        {'number': '2', 'title': 'По убыв. цены', 'order': '-price'},

    ]

    cats = Category.objects.annotate(cnt=Count('goods')).order_by('id')
    current_select_item = request.POST.get('shop_goods_start_with')
    goods = get_good(slug_cat, current_select_item, select_items)
    paginator = Paginator(goods, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    images = Gallery.objects.all()
    sps = {}
    for i in images:
        sps[i.good.pk] = i.image.url
    print(sps)
    plh = 'https://via.placeholder.com/320x320'
    context = {
        'menu': menu,
        'cats': cats,
        'goods': page_obj,
        'select_items': select_items,
        'now_item': current_select_item,
        'sps': sps,
        'plh': plh,
        # 'page_obj': page_obj
    }

    return render(request, 'UralsSteelStore/shop_catalog.html', context=context)

# class ShopCatalogListView(ListView):
#     model = Goods
#     template_name = 'UralsSteelStore/shop_catalog.html'
#     context_object_name = 'goods'
#     paginate_by = 9
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ShopCatalogListView, self).get_context_data(object_list=None, **kwargs)
#         context['cats'] = Category.objects.annotate(cnt=Count('goods')).order_by('id')
#         context['current_select_item'] = self.request.POST.get('shop_goods_start_with')
#         context['menu'] = menu
#         context['select_items'] = select_items
#         images = Gallery.objects.all()
#         sps = {}
#         for i in images:
#             sps[i.good.pk] = i.image.url
#         context['sps'] = sps
#         return context
#
#     def post(self, request, *args, **kwargs):
#         if request.POST.get('shop_goods_start_with'):
#             goods = get_good(self.kwargs.get('slug_cat'), self.request.POST.get('shop_goods_start_with'), select_items)
#         return goods

    def get_queryset(self):
        goods = get_good(self.kwargs.get('slug_cat'), self.request.POST.get('shop_goods_start_with'), select_items)
        return goods


def about_good(request, slug_cat=None, slug_good_name=None, current_img=None):
    context = {}
    context['menu'] = menu
    images = Gallery.objects.filter(good__slug=slug_good_name)[::-1]
    context['images'] = images

    if current_img != None:
        current_img = current_img.replace('-', '/').replace('_', '.')

        context['current_img'] = current_img
    else:

        if len(images) != 0:
            current_img = images[0].image.url
            context['current_img'] = current_img
        else:
            current_img_base = r'D:\MY DJANGO PROJECTS\SteelofhteUrals\UralsSteel\media\base_img.png'
            context['current_img_base'] = current_img_base

    good = Goods.objects.filter(slug=slug_good_name)
    context['good'] = good

    some_goods = Goods.objects.filter(category__title=good[0].category)[1:5]
    context['some_goods'] = some_goods

    images_for_some_goods = Gallery.objects.all()
    sps = {}
    for i in images_for_some_goods:
        sps[i.good.pk] = i.image.url
    context['sps'] = sps

    return render(request, 'UralsSteelStore/about_good.html', context=context)


def about_us(request):
    context = {
        'menu': menu,
    }
    return render(request, 'UralsSteelStore/about_us.html', context=context)


class About_Us_TemplateView(TemplateView):
    template_name = 'UralsSteelStore/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu

        return context


def contacts_ways(request):
    context = {
        'menu': menu,
    }
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = RequestForm()
    context['form'] = form

    return render(request, 'UralsSteelStore/contacts_ways.html', context=context)


@login_required(login_url='users:registration')
def basket(request):
    context = {'menu': menu, 'baskets': Basket.objects.filter(user=request.user), }

    if request.method == 'POST':
        form = BasketRequestForm(request.POST)
        if form.is_valid():
            print(memory['good_id_to_basket'], form.cleaned_data)
            orders_id = random.randint(3000, 10000)
            Orders.objects.create(
                orders_id=orders_id,
                id_of_products=[order for order in memory['good_id_to_basket']],
                customer_name=form.cleaned_data['full_name'],
                customer_email=form.cleaned_data['email'],
                customer_pay_way=form.cleaned_data['pay_radio'],
                customer_delivery_way=form.cleaned_data['delivery_radio'],
                customer_comment_to_order=form.cleaned_data['comment'],
                customer_phone_number=form.cleaned_data['phone_number'],
                customer_data_processing=form.cleaned_data['checkb'],
                user=request.user
            )
            baskets = Basket.objects.filter(user=request.user)
            for basket in baskets:
                basket.delete()
            return render(request, 'UralsSteelStore/success_order.html', context={'menu': menu, 'orders_id': orders_id})
            # context['order_number'] = random.randint(50000, 1346641)
    else:
        form = BasketRequestForm()
    context['form'] = form
    return render(request, 'UralsSteelStore/basket.html', context=context)


@login_required(login_url='users:registration')
def basket_add(request, product_id):
    product = Goods.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_quantity_remove(request, product_id=None):
    product = Goods.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    basket = baskets.first()
    if basket.quantity == 1:
        basket.delete()
    else:
        basket.quantity -= 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove_all(request):
    baskets = Basket.objects.filter(user=request.user)
    for basket in baskets:
        basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# def index(request, category_id=1):
#     if request.method == 'POST':
#         form = ModalRequestForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#     else:
#         form = ModalRequestForm()
#
#     all_categories = Category_mp.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)
#
#
#     products = Products.objects.filter(category=category_id)
#     naw_cat = Category_mp.objects.get(pk=category_id)
#
#     context = {
#         'products': products,
#         'all_categories': all_categories,
#         'menu': menu,
#         'naw_cat': naw_cat,
#         'form': form
#     }
#     if memory['basket_total_price']:
#         context['basket_total_price'] = memory['basket_total_price']
#
#     return render(request, 'UralsSteelStore/index.html', context=context)
# def services(request):
#     if request.method == 'POST':
#         form = ModalRequestForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#     else:
#         form = ModalRequestForm()
#
#     context = {'menu': menu, 'form': form}
#     if memory['basket_total_price']:
#         context['basket_total_price'] = memory['basket_total_price']
#     return render(request, 'UralsSteelStore/services.html', context=context)
# def basket(request):
#
#     context = {
#         'menu': menu
#     }
#     # if 'good_id_to_basket' in memory:
#     #     context['good_id_to_basket'] = memory['good_id_to_basket']
#
#     if len(memory['good_id_to_basket']) > 0:
#         basket_items = []
#         for i in memory['good_id_to_basket']:
#             item = Goods.objects.get(pk=i)
#             basket_items.append(item)
#             print(basket_items)
#
#         context['good_id_to_basket'] = basket_items
#         context['basket_len'] = len(memory['good_id_to_basket'])
#
#         basket_total_price = 0
#         for i in basket_items:
#             basket_total_price += i.price
#         context['basket_total_price'] = basket_total_price
#         memory['basket_total_price'] = basket_total_price
#         context['good_id_to_basket_mes'] = 'basket_is_full'
#     else:
#         context['basket_total_price'] = 0
#         context['good_id_to_basket_mes'] = 'basket_is_empty'
#         context['basket_len'] = 0
#
#     print(context)
#
#     if request.POST.get('basket_item_del_btn'):
#         good_for_del = request.POST.get('basket_item_del_btn')
#         print('good_for_del', good_for_del)
#         begine = memory['good_id_to_basket']
#         try:
#             begine.remove(good_for_del)
#         except ValueError:
#             print('Item not in list')
#         memory['good_id_to_basket'] = begine
#         return redirect(request.META['HTTP_REFERER'])
#
#     if request.POST.get('clean_basket'):
#         begine = memory['good_id_to_basket']
#         try:
#             begine.clear()
#         except:
#             print('Item not in list')
#         memory['good_id_to_basket'] = begine
#         memory['basket_total_price'] = 0
#         return redirect(request.META['HTTP_REFERER'])
#
#     # if request.method == 'POST':
#     #     form = RequestForm(request.POST)
#     #     if form.is_valid():
#     #         print(form.cleaned_data)
#     # else:
#     #     form = RequestForm()
#     #
#     # context['form'] = form
#
#     if request.method == 'POST':
#         form = BasketRequestForm(request.POST)
#         if form.is_valid():
#             print(memory['good_id_to_basket'], form.cleaned_data)
#
#             # df = pd.DataFrame({
#             #                     'Номер заказа': random.randint(3000, 10000),
#             #                    'ID товаров': [order for order in memory['good_id_to_basket']],
#             #                    'Доставка': form.cleaned_data['delivery_radio'],
#             #                    'Оплата': form.cleaned_data['pay_radio'],
#             #                    'Имя': form.cleaned_data['full_name'],
#             #                    'Email': form.cleaned_data['email'],
#             #                    'Номер телефона': form.cleaned_data['phone_number'],
#             #                    'Комментарий к заказу': form.cleaned_data['comment'],
#             #                    'Обработка данных': form.cleaned_data['checkb'],
#             #                    })
#             # df.to_excel('./orders_list.xlsx')
#             Orders.objects.create(
#                 orders_id=random.randint(3000, 10000),
#                 id_of_products=[order for order in memory['good_id_to_basket']],
#                 customer_name=form.cleaned_data['full_name'],
#                 customer_email=form.cleaned_data['email'],
#                 customer_pay_way=form.cleaned_data['pay_radio'],
#                 customer_delivery_way=form.cleaned_data['delivery_radio'],
#                 customer_comment_to_order=form.cleaned_data['comment'],
#                 customer_phone_number=form.cleaned_data['phone_number'],
#                 customer_data_processing=form.cleaned_data['checkb'],
#             )
#
#
#             memory['good_id_to_basket'].clear()
#             memory['basket_total_price'] = 0
#             return redirect(request.path)
#             # context['order_number'] = random.randint(50000, 1346641)
#     else:
#         form = BasketRequestForm()
#
#
#     context['form'] = form

# return render(request, 'UralsSteelStore/basket.html', context=context)


# class RegisterUser(CreateView):
#     """Класс регистрации пользователей, при успешной регистрации пользователь автоматически авторизуется благодаря
#     методу form_valid"""
#
#     form_class = RegistrationUserForm
#     template_name = 'UralsSteelStore/registration.html'
#     success_url = reverse_lazy('authorisation')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         if memory['basket_total_price']:
#             context['basket_total_price'] = memory['basket_total_price']
#         return context
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')
# class AuthorisationUser(LoginView):
#     """Класс авторизации пользователей, при успешной авторизации перенаправляет на первую страницу"""
#
#     form_class = AuthorisationUserForm
#     template_name = 'UralsSteelStore/authorisation.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         if memory['basket_total_price']:
#             context['basket_total_price'] = memory['basket_total_price']
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('home')
# def logout_user(request):
#     """Выход пользователя из авторизованного состояния"""
#     logout(request)
#     memory['good_id_to_basket'] = []
#     memory['basket_total_price'] = 0
#
#     return redirect('authorisation')
