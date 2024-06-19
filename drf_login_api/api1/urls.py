from django.urls import path
from .views import CustomAuthToken, AddCustomerView, GetCustomerView, EditCustomerView, ChangePasswordView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('add_customer/', AddCustomerView.as_view(), name='add_customer'),
    path('get_customer/<int:id>/', GetCustomerView.as_view(), name='get_customer'),
    path('edit_customer/<int:id>/', EditCustomerView.as_view(), name='edit_customer'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]