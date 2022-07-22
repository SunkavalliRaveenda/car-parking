

from django.urls import path

from . import views
urlpatterns = [
    path('', views.SlotAvailableListing.as_view(), name='index'),
    path('slot', views.SlotListApiView.as_view(),name=""),
    path('slot/<int:slot_id>/', views.SlotDetailApiView.as_view()),
    path('book', views.BookListApiView.as_view(),name="booking"),
    path('book/<int:pk>/', views.BookDetailApiView.as_view({"post": "update"}),name="booking-edit"),
]