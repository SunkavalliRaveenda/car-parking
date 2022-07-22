from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
def index(request):
    return render(request=request,template_name='index.html',context={})

class MyBookingView(View):
    template_name = 'booking/list.html'
    
    def get(self,request):
        return render(request, self.template_name)