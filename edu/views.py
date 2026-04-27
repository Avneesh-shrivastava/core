from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def student_login(request):
    return render(request, 'login.html')

def student_signup(request):
    if request.method == 'POST':
        data = request.POST

        global st_username
        global st_password

        st_name = data.get('fullname')
        st_email = data.get('email')
        st_username = data.get('username')
        st_password = data.get('password')
        st_confirm_pass = data.get('confirm_password')

        if st_password == st_confirm_pass:
            student_signup_data.objects.create(
                st_name = st_name,
                st_email = st_email,
                st_username = st_username,
                st_password = st_password,
                st_confirm_pass = st_confirm_pass
                )

            view_data = student_signup_data.objects.all().values()
            print(view_data)

        if st_password != st_confirm_pass:
            messages.error(request, "Password did not matched")
            print(st_password)
            print(st_confirm_pass)
            return render(request, 'signup.html')

        print(st_password)
        print(st_confirm_pass)
        
        return redirect('/student-login/')
    return render(request, 'signup.html')

def show_data(request):
    queryset = student_signup_data.objects.all()
    context = {'students_data' : queryset}
    return render(request, 'show_data.html', context)

def delete_data(request, id):
    that_data = student_signup_data.objects.get(id=id)
    that_data.delete()
    return redirect('/show-data/')

def student_login(request):
    if request.method == 'POST':
        data = request.POST
        log_username = data.get('username')
        log_password = data.get('password')
        
    return render(request, 'login.html')