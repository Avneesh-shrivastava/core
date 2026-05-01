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

        if st_password and st_confirm_pass:
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
            return render(request, 'signup.html')
        
        username_column = student_signup_data.objects.values('st_username')

        if {'st_username':f'{st_username}'} in username_column :
            messages.error(request, "This username already exist's")
            return render(request, 'signup.html')


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
        global st_username
        global st_password
        data = request.POST
        log_username = data.get('username')
        log_password = data.get('password')
        
        username_list = student_signup_data.objects.values('st_username')
        password_list = student_signup_data.objects.values('st_password')

        if {'st_username': f'{log_username}'} in username_list and {'st_password': f'{log_password}'} in password_list :
            return render(request, 'home_page.html')       
        
    return render(request, 'login.html')

def home_page(request):
    return render(request, 'home_page.html')

def courses(request):
    return render(request, 'courses.html')

def search_results(request):
    
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        results = Subjects_details.objects.filter(course_name__icontains=search_query)
        print(results)
    # course_data =  Subjects_details.objects.all().values()
    context = {'course_data' : results}
    return render(request, 'search_results.html', context)