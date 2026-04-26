from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def receipes(request):
    if request.method == "POST":
        data = request.POST
        image = request.FILES

        receipe_image = image.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_desc')

        print(receipe_name)
        print(receipe_description)
        print(receipe_image)

        Receipe.objects.create(
            receipe_name = receipe_name,
            receipe_desc = receipe_description,
            receipe_image = receipe_image
        )


        return redirect('/receipes/')
    query_set = Receipe.objects.all()
    context = {'receipe' : query_set}
    return render(request, 'receipes.html', context)

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')

def update_receipe(request, id):
    if request.method == "POST":
        data = request.POST
        image = request.FILES
        updt_name = data.get('updt_name')
        updt_desc = data.get('updt_desc')
        updt_image = image.get('updt_img')

        queryset = Receipe.objects.get(id = id)
        
        if updt_name != "":
            queryset.receipe_name = updt_name
            print('name is not none')
        if updt_desc != "":
            queryset.receipe_desc = updt_desc
            print('desc is not none')
        if updt_image:
            queryset.receipe_image = updt_image
            print('image is not none')

        
        print(updt_name)
        print(updt_desc)
        print(updt_image)

        queryset.save()
        return redirect('/receipes/')
    
    return render(request, 'update_data.html')