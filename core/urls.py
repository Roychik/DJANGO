from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserRetriveUpdateDestroyAPIView.as_view(), name='user_detail'),
    path('users/create-random', UserRandomCreateView.as_view(), name='users_random_create'),
    path('banks/', BankListCreateAPIView.as_view(), name='banks_list'),
    path('banks/<int:pk>/', BankRetriveUpdateDestroyAPIView.as_view(), name='bank_detail'),
    path('banks/create-random', BankRandomCreateView.as_view(), name='banks_random_create'),
    path('users/<int:user_id>/banks/<int:bank_id>/', UserBankView.as_view(), name='user_bank'),
]