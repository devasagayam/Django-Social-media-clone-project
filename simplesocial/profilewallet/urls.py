from django.contrib import admin
from django.urls import path,include
from profilewallet import views

app_name='wallet'

urlpatterns = [
    path('',views.CreateWallet.as_view(), name='create_wallet'),

]
