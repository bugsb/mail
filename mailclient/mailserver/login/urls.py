from django.urls import path,include
from . import views

urlpatterns = [
 path('', views.login,name="Login"),
 path('signup/', views.signup,name="SignUp"),
 path('login/', views.login,name="login"),
 path('logout/', views.logout,name="Logout"),
 path('resetpass/', views.resetpass,name="Reset Pass"),
 path('pass/', views.password,name="Pass"),
 ]
