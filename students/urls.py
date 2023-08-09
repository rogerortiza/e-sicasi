from django.urls import path
from .views import *


urlpatterns = [
    path("register/", StudentRegistrationView.as_view(), name="student-registration"),
]
