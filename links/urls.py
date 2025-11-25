from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_page, name='public_page'),
    path('login/', views.login_view, name='login'),
# uncomment the url below to allow self registration
#    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]