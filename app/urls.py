from django.urls import path
from .views import root,validate,email

urlpatterns = [
    path('',root,name="root"),
    path('validate/',validate,name="validate"),
    path('email/',email,name="email")
]
