
from datetime import datetime, timedelta
from functools import partial
from account.models import Profile
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from slot_api.models import Booking, Slot
from slot_api.serializers import BookingSerializer, BookingSerializerExtended, SlotSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from account.auth_backend import PasswordlessAuthBackend
from django.contrib.auth import login
from rest_framework import viewsets

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the Slot_API index.")


class SlotListPagination(PageNumberPagination):
    page_size = 10


class SlotAvailableListing(ListAPIView):
    pagination_class = SlotListPagination
    serializer_class = SlotSerializer

    def get_queryset(self):
        slots = Slot.objects.all()
        return slots


class SlotListApiView(APIView):
    def get(self, request, *args, **kwargs):
        slots = Slot.objects.all()
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'title': request.data.get('title'),

        }
        serializer = SlotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlotDetailApiView(APIView):
    def get_object(self, slot_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Slot.objects.get(id=slot_id)
        except Slot.DoesNotExist:
            return None

    def get(self, request, slot_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        slot_instance = self.get_object(slot_id)
        if not slot_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SlotSerializer(slot_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, slot_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        slot_instance = self.get_object(slot_id, )
        if not slot_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),

        }
        serializer = SlotSerializer(
            instance=slot_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, slot_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(slot_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class BookListApiView(APIView):
   
    def get(self, request, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
       
        book_instance = Booking.objects.all()
        serializer = BookingSerializerExtended(book_instance,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        
        if request.user.is_authenticated and request.data.get('email') == request.user.email:
            print('is_authenticated')
            user = request.user
        else:
            authBackend = PasswordlessAuthBackend()
            print(' not is_authenticated')
            users=Profile.objects.filter(email=request.data.get('email'))
            print(users)
            if users.exists():
                print(' not is_authenticated exists')
                user = users.first()
                user = authBackend.authenticate(email=user.email)
            else:

                user= Profile.objects.create(email=request.data.get('email'),name=request.data.get('name'))
                user = authBackend.authenticate(email=user.email)
            login(
                    request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
        data = {
            'car_name': request.data.get('car_name'),
            'user':user.id,
            'slot':request.data.get('slot_id'),
            'start_time':datetime.now(),
            'end_time':datetime.now()+timedelta(hours=4)

        }
        serializer = BookingSerializer(data=data,partial=True)
        if serializer.is_valid():
            booking = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    





class BookDetailApiView(viewsets.ModelViewSet):
    def get_object(self, id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Booking.objects.get(id=id)
        except Slot.DoesNotExist:
            return None
    def get(self, request, pk, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        book_instance = self.get_object(pk)
        if not book_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingSerializerExtended(book_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # def post(self, request, *args, **kwargs):
    #     print(request.user.is_authenticated)
        
    #     if request.user.is_authenticated and request.data.get('email') == request.user.email:
    #         print('is_authenticated')
    #         user = request.user
    #     else:
    #         authBackend = PasswordlessAuthBackend()
    #         print(' not is_authenticated')
    #         users=Profile.objects.filter(email=request.data.get('email'))
    #         print(users)
    #         if users.exists():
    #             print(' not is_authenticated exists')
    #             user = users.first()
    #             user = authBackend.authenticate(email=user.email)
    #         else:

    #             user= Profile.objects.create(email=request.data.get('email'),name=request.data.get('name'))
    #             user = authBackend.authenticate(email=user.email)
    #         login(
    #                 request,
    #                 user,
    #                 backend="django.contrib.auth.backends.ModelBackend",
    #             )
    #     data = {
    #         'car_name': request.data.get('car_name'),
    #         'user':user.id,
    #         'slot':request.data.get('slot_id'),
    #         'start_time':datetime.now(),
    #         'end_time':datetime.now()+timedelta(hours=4)

    #     }
    #     serializer = BookingSerializer(data=data,partial=True)
    #     if serializer.is_valid():
    #         booking = serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        book_instance = self.get_object(pk)
        if not book_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data.get('type')=="reallocate":
            data = {
                'start_time':datetime.now(),
                'end_time':datetime.now()+timedelta(hours=4)

            }
        else:
            data = {
                'status': request.data.get('status'),
            }
        serializer = BookingSerializer(
            instance=book_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



