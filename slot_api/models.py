from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Profile

# Create your models here.
class Slot(models.Model):
    options = (
        ("available", "Available"),
        ("occupied", "Occupied"),
    )
    title=models.CharField(max_length = 180)
    status=models.CharField(max_length=10, choices=options, default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    options = (
        ("available", "Available"),
        ("occupied", "Occupied"),
        ("vaccant", "Vaccant"),
    )
    user = models.ForeignKey(Profile, on_delete = models.CASCADE,related_name="bookings")
    slot = models.ForeignKey(Slot, on_delete = models.CASCADE,related_name="bookings")
    car_name=models.CharField(null=True, blank=True, max_length=120)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status=models.CharField(max_length=10, choices=options, default="occupied")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver([post_save], sender=Booking)
def save_booking(sender, instance, **kwargs):
    
    slot = instance.slot
    print(slot.status)
    if instance.status=='vaccant':
        slot.status="available" 
        slot.save()
    else:
        slot.status="occupied" 
        slot.save()
    print(slot.status)