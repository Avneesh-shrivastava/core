from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from .models import *

def students(request):
    if request.method == "POST":
        data = request.POST
        name  = data.get('name')
        email_id = data.get('email_id')
        phone_no = data.get('phone_no')
        address = data.get('address')
        reason = data.get('reason')

        print(name)
        print(email_id)
        print(phone_no)
        print(address)
        print(reason)

        Students_data.objects.create(
            name = name,
            email_id = email_id,
            phone_no = phone_no,
            address = address,
            reason = reason
        )
        
        return redirect('/students/')
    return render(request, 'form_fill.html')