from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('botuser',BotUserViewset)
router.register('channels',TelegramChannelViewset)
router.register('category',CategoryViewset)
router.register('subcategory',SubCategoryViewset)
router.register('product',ProductViewset)
router.register('order',OrderViewset)
router.register('orderitem',OrderItemViewset)
urlpatterns=[
    path('',include(router.urls)),
    path('user/',GetUser.as_view()),
    path('lang/',ChangeUserLanguage.as_view()),
    path('channel/',GetTelegramChannel.as_view()),
    path('delete_channel/',DeleteTelegramChannel.as_view()),
    path('phone/', ChangePhoneNumber.as_view()),
    path('type/', ChangeType.as_view()),
    path('address/', ChangeAddress.as_view()),
    path('shop/', OrderedItems.as_view()),
    path('set_order/', SetOrderItem.as_view()),
    path('create_order/', Order7foodCreateView.as_view()),
    path('saboy-create/', Order7foodSaboyCreateView.as_view()),
    path('delete_basket/', DestroyBasket.as_view()),
    path('delete_item/', DeleteItem.as_view()),
    path('user_info/',BotUserInfo.as_view()),
    path('total_order_time/', TotalOrderTimeView.as_view(), name='total-order-time'),
    path('orders_web/', order_table_list_view, name='order_table_list'),
    path('orders_web/new/', create_order_view, name='create_order'),
]
