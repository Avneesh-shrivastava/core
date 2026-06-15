from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
def student_login(request):
    return render(request, 'login.html')

def student_signup(request):
    if request.method == 'POST':
        data = request.POST

        st_name = data.get('fullname')
        st_email = data.get('email')
        st_username = data.get('username')
        st_password = data.get('password')
        st_confirm_pass = data.get('confirm_password')
        
        user = User.objects.filter(username = st_username)

        if user.exists():
            messages.error(request, "This username already exists")
            return redirect('/student-signup/')
            
        if st_password != st_confirm_pass:
            messages.error(request, "Password did not matched")
            return render(request, 'signup.html')

        user = User.objects.create(
            first_name = st_name,
            email = st_email,
            username = st_username,
            )
        
        user.set_password(st_password)
        user.save()

        view_data = User.objects.all().values()
        print(view_data)

        return redirect('/student-login/')
    return render(request, 'signup.html')

def show_data(request):
    queryset = User.objects.all()
    context = {'students_data' : queryset}

    return render(request, 'show_data.html', context)

def delete_data(request, id):
    that_data = User.objects.get(id=id)
    that_data.delete()
    return redirect('/show-data/')

def student_login(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        if not User.objects.filter(username = username).exists() :
            messages.info(request, "Username does not exists")
            return redirect('/student-login/')

        user = authenticate(request, username = username, password = password) 
        #this authincate code will check from the database by running (User.objects.get(username=username) and will return True if exists and false if not) 

        if user is None:
            messages.info(request, "Invalid password")
            return redirect('/student-login/')
        else:
            login(request, user)
            return redirect('/home-page/')
        
        return redirect('/student-login/')        
        
    return render(request, 'login.html')

def home_page(request):
    return render(request, 'home_page.html')

def courses(request):
    sub = ''

    if request.GET.get('Accountancy'):
        sub = request.GET.get('Accountancy')

    if request.GET.get('Business Studies'):
        sub = request.GET.get('Business Studies')

    if request.GET.get('Economics'):
        sub = request.GET.get('Economics')

    if request.GET.get('English'):
        sub = request.GET.get('English')

    subjects = Subjects_details.objects.all().filter(course_name__icontains = sub)

    context = {'subjects': subjects }
    
    return render(request, 'courses.html', context)

def search_results(request):
    queryset =  Subjects_details.objects.all()
    search_query = ''
    message = ''

    if request.GET.get('search'):
        search_query = request.GET.get('search')
        # if search_query == 'accounts' or search_query == 'acc' or search_query == 'accountancy' or search_query == 'Accountancy':
        #     proper_search_name = 'Accountancy'

        from django.db.models import Q
        queryset = queryset.filter(Q(course_name__icontains = search_query))
        print(queryset)

        results_no = len(queryset)
        print(results_no)
    # course_data =  Subjects_details.objects.all().values('course_name')
    # print(course_data)

    message = 'Showing results for '
    if not queryset:
        queryset =  Subjects_details.objects.all()
        message = 'Result not found for '
    if not search_query :
        queryset =  Subjects_details.objects.all()
        message = 'Result not found'

    print(search_query)
    context = {'search_name' : search_query, 'course_data' : queryset, 'message' : message, 'results_no' : results_no}

    return render(request, 'search_results.html', context)

def enrollment_form(request):
    return render(request, 'enrollment.html')

def log_out(request):
    return redirect('/student-login/')