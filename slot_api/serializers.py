
from rest_framework import serializers
from slot_api.models import Booking, Slot


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        # depth=2


class BookingSerializerExtended(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields="__all__"
        depth=2