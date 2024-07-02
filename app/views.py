from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import filters
from .utils import Sum_all_order_time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


class BotUserViewset(ModelViewSet):
    queryset = BotUserModel.objects.all()
    serializer_class = BotUserSerializer

class TotalOrderTimeView(APIView):
    def get(self, request):
        total_time = Sum_all_order_time()
        return Response({"total_time": total_time})

class GetUser(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class ChangeUserLanguage(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                user.language = data['language']
                user.save()
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class TelegramChannelViewset(ModelViewSet):
    queryset = TelegramChannelModel.objects.all()
    serializer_class = TelegramChannelSerializer
class DeleteTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id', None):
            try:
                user = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                user.delete()
                return Response({'status':"Deleted"},status=status.HTTP_200_OK)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
class GetTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id',None):
            try:
                channel = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                serializer = TelegramChannelSerializer(channel, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
# #################
class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SubCategoryViewset(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price', 'about']


class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewset(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


from rest_framework.views import APIView

class ChangePhoneNumber(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()
        telegram_id = data['telegram_id']
        user = BotUserModel.objects.get(telegram_id=telegram_id)
        user.phone = data['phone']
        user.save()
        return Response({'status': 'Phone Number changed.'})

class ChangeType(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()
        telegram_id = data['telegram_id']
        user = BotUserModel.objects.get(telegram_id=telegram_id)
        user.type = data['type']
        user.save()
        return Response({'status': 'Type  changed.'})
class ChangeAddress(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()
        telegram_id = data['telegram_id']
        user = BotUserModel.objects.get(telegram_id=telegram_id)
        user.latitude = data['latitude']
        user.longitude = data['longitude']
        user.save()
        return Response({'status': f"Address changed."})


class OrderedItems(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()
        user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class SetOrderItem(APIView):
    def post(self, request):
        data = request.POST
        data = data.dict()

        telegram_id = data['telegram_id']
        product = data['product']
        quantity = data['quantity']
        user = BotUserModel.objects.get(telegram_id=telegram_id)
        product = Product.objects.get(id=product)
        order, created = Order.objects.get_or_create(user=user)

        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if int(quantity) == 0:
            orderitem.delete()
            return Response({'status': 'Order Item Deleted'})
        else:
            orderitem.quantity = quantity
            orderitem.save()
            return Response({'status': 'Order Item Updated'})


class DestroyBasket(APIView):
    def post(self, request):
        data = request.data
        data = data.dict()
        telegram_id = data['telegram_id']
        user = BotUserModel.objects.get(telegram_id=telegram_id)
        try:
            order = Order.objects.get(user=user)
            order.delete()

        except Order.DoesNotExist:
            pass
        except Exception as e:
            pass
        return Response({'status': 'Basket Deleted'})


class DeleteItem(APIView):
    def post(self, request):
        data = request.data
        data = data.dict()
        telegram_id = data['telegram_id']
        product = data['product']
        user = BotUserModel.objects.get(telegram_id=telegram_id)
        product = Product.objects.get(id=product)
        order, created = Order.objects.get_or_create(user=user)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderitem.delete()
        return Response({'status': "Order Item deleted"})
def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response
class BotUserInfo(APIView):
    def post(self,request):
        data = request.data
        botuser = BotUserModel.objects.get(telegram_id = data['telegram_id'])
        serializer=  BotUserSerializer(instance=botuser,partial=True)
        return Response(serializer.data)




from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from app.serializer import *

class Order7foodCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Order7foodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Order7foodSaboyCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Order7foodSaboySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderTable, Product, OrderTableItem
from .forms import OrderTableForm, OrderTableItemForm
from django.forms import inlineformset_factory

def order_table_list_view(request):
    orders = OrderTable.objects.all()
    return render(request, 'ordertable.html', {'orders': orders})

def create_order_view(request):
    OrderTableItemFormSet = inlineformset_factory(OrderTable, OrderTableItem, fields=('product', 'quantity'), extra=1, can_delete=True)
    if request.method == 'POST':
        order_form = OrderTableForm(request.POST)
        formset = OrderTableItemFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save()
            formset.instance = order
            formset.save()
            return redirect('order_table_list')
    else:
        order_form = OrderTableForm()
        formset = OrderTableItemFormSet()
    return render(request, 'createtable.html', {'order_form': order_form, 'formset': formset})


