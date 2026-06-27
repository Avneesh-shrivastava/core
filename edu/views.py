from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
# def student_login(request):
#     return render(request, 'login.html')

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

@login_required(login_url='/student-login/')
def home_page(request):
    no_of_enrolled = enrollment_data.objects.all()
    no_of_enrolled = len(no_of_enrolled)

    subjects = Subjects_details.objects.values_list('course_name', flat=True)
    enrolled_subjects = enrollment_data.objects.values_list('course', flat=True)

    context = {"no_of_enrolled" : no_of_enrolled, "subjects" : subjects, "enrolled_subjects": enrolled_subjects}
    return render(request, 'home_page.html', context)


@login_required(login_url='/student-login/')
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

    print("Subjects_details = ",subjects.values_list('course_name', flat=True))
    print('\n')
    enrolled_subject = enrollment_data.objects.values_list('course', flat=True)
    print("enrollment_data = ",enrolled_subject.values())
    print('\n')
    courses = Course.objects.all()
    print("Course = ",courses.values())
    print('\n')
    print("user_n_courses = ", user_n_course.objects.values())
    print('\n')
    # list = []
    enrolled_course_ids = user_n_course.objects.filter(user_id=request.user).values_list('course_id', flat=True)
    print('enrolled_course_ids = ',enrolled_course_ids)
    print('\n')
    # print(courses.values())
    #list.append(enrolled_course_ids)
    # print(list)
    # print(user_n_course.objects.values_list('course_id', flat=True))
    # print(user_n_course.objects.filter(user_id=request.user).values_list('course_id', flat=True))

    # print(Course.objects.values_list('id', flat=True))

    context = {'subjects': subjects, "enrolled_subject" : enrolled_subject, 'enrolled_course_ids': enrolled_course_ids , 'courses' : courses}

    return render(request, 'courses.html', context)

@login_required(login_url='/student-login/')
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

@login_required(login_url='/student-login/')
def enrollment_form(request):
    # u_n_c = user_n_course.objects.values()
    enrolled_course_ids = user_n_course.objects.filter(user_id=request.user).values_list('course_id', flat=True)
    enrolled_course_ids = list(enrolled_course_ids)

    try:
        if request.method == 'POST':
    
            data = request.POST
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            dob = data.get('dob')
            gender = data.get('gender')
            current_class = data.get('current_class')
            school = data.get('school')

            course_id = data.get('course')
            course = Course.objects.get(id=course_id)

            parent_name = data.get('parent_name')
            parent_phone = data.get('parent_phone')
            address = data.get('address')
            message = data.get('message')

            

            if course_id in enrolled_course_ids:

                # enrollment_data.objects.create(
                #     user = request.user,
                #     first_name = first_name,
                #     last_name = last_name,
                #     email = email,
                #     phone = phone,
                #     dob = dob,
                #     gender = gender,
                #     current_class = current_class,
                #     school = school,
                #     course = data.get('course_name'),
                #     parent_name = parent_name,
                #     parent_phone = parent_phone,
                #     address = address,
                #     message = message
                # )
                
                # user_n_course.objects.create(
                #     user = request.user,
                #     course = course
                # )
                print("Data created")

            # u_n_c = user_n_course.objects.values()
            # print(u_n_c)

            # print(enrollment_data.objects.values())
            
            else:
                print("Data not Created") 
                print(course_id)
                print(enrolled_course_ids)   
            return redirect('/home-page/')
    except ValueError:
        messages.info(request, "Please Fill the form first")
        return redirect('/enrollment/')

    print(enrollment_data.objects.values())
    courses = Course.objects.all()
    

    if course_id in enrolled_course_ids:
        print('yes')


    return render(request, 'enrollment.html', {'courses' : courses})

def log_out(request):
    logout(request)
    return redirect('/student-login/')

def curriculum(request, id):
    students_enrolled = enrollment_data.objects.all()
    students_enrolled = len(students_enrolled)

    course = Course.objects.get(id=id)

     
    subject_enrolled = enrollment_data.objects.values_list('course', flat=True)
    print(subject_enrolled)
    
    context = {"students_enrolled" : students_enrolled, "course" : course}

    return render(request, 'curriculum.html', context)