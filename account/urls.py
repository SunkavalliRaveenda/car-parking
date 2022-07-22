from account.views import LoginApiView, SignUpView, myBookingsListing

from django.urls import path


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('index', myBookingsListing.as_view(), name='index'),
    path('login', LoginApiView.as_view(), name='login'),
]