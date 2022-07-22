from django.contrib import admin

from slot_api.models import Booking, Slot

# Register your models here.
class SlotAdmin(admin.ModelAdmin):
    list_display = ('id','title','status',)
    list_filter = ('status', )


admin.site.register(Slot,SlotAdmin)

admin.site.register(Booking)