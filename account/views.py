from django.shortcuts import render
from django.views.generic import CreateView

from account.forms import CustomUserCreationForm, SignUpForm
from django.urls import reverse_lazy
from account.models import Profile
from account.serializers import ProfileSerializer
from rest_framework.pagination import PageNumberPagination
from slot_api.models import Booking
from slot_api.serializers import BookingSerializerExtended
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from account.auth_backend import PasswordlessAuthBackend
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class BListPagination(PageNumberPagination):
    page_size = 10


class SignUpView(CreateView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('webapp:index')
    form_class = CustomUserCreationForm


class LoginApiView(APIView):

    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''

        authBackend = PasswordlessAuthBackend()
        users = Profile.objects.filter(email=request.data.get('email'))
        print(users)
        if users.exists():
            user = users.first()
            user = authBackend.authenticate(email=user.email)
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend",
            )
            serializer = ProfileSerializer(user)
            return Response({"data":serializer.data,"success":True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"data":f"No Bookings found with {request.data.get('email')} Try Again with different email","success":False},
                status=status.HTTP_200_OK
            )


class myBookingsListing(ListAPIView):

    pagination_class = BListPagination
    serializer_class = BookingSerializerExtended

    def get_queryset(self):
        if self.request.user.is_authenticated:
            bookings = Booking.objects.filter(user=self.request.user,status='occupied')
            # bookings.update(status='occupied')
        else:
            bookings = Booking.objects.filter(user_id=None)
        return bookings
