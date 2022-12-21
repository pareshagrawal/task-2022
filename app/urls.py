from django.urls import path
from .views import root,validate

urlpatterns = [
    path('',root,name="root"),
    path('validate/',validate,name="validate")
]
