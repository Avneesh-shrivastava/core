from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
from django.core.mail import send_mail

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

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

# def show_data(request):
#     queryset = User.objects.all()
#     context = {'students_data' : queryset}

#     return render(request, 'show_data.html', context)

# def delete_data(request, id):
#     that_data = User.objects.get(id=id)
#     that_data.delete()
#     return redirect('/show-data/')

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

    # print("Subjects_details = ",Course.objects.values_list('subject_name', flat=True))
    print('\n')
    enrolled_subject = enrollment_data.objects.values_list('course', flat=True)
    # print("enrollment_data = ",enrolled_subject.values())
    print('\n')
    courses = Course.objects.all()
    # print("Course = ",courses.values())
    print('\n')
    # print("user_n_courses = ", user_n_course.objects.values())
    print('\n')
    # list = []
    enrolled_course_ids = user_n_course.objects.filter(user_id=request.user).values_list('course_id', flat=True)
    print('enrolled_course_ids = ',enrolled_course_ids)
    print('\n')

    # print("Modules = ", Module.objects.values())
    # print("\n")
    print("Topic = ", Topic.objects.values())
    # print("\n")
    print("Topic_link = ", topic_links.objects.values())

    context = {'subjects': subjects, "enrolled_subject" : enrolled_subject, 'enrolled_course_ids': enrolled_course_ids , 'courses' : courses}

    return render(request, 'courses.html', context)

@login_required(login_url='/student-login/')
def search_results(request):
    queryset =  Subjects_details.objects.all()
    search_query = ''
    message = ''
    results_no = 0

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

            course_id = int(course_id)

            if course_id not in enrolled_course_ids:

                enrollment_data.objects.create(
                    user = request.user,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone = phone,
                    dob = dob,
                    gender = gender,
                    current_class = current_class,
                    school = school,
                    course = data.get('course_name'),
                    parent_name = parent_name,
                    parent_phone = parent_phone,
                    address = address,
                    message = message
                )
                
                user_n_course.objects.create(
                    user = request.user,
                    course = course
                )

                u_n_c = user_n_course.objects.values()
                print(u_n_c)
                print("\n")

                print(enrollment_data.objects.values())

                # send_mail(
                #     'Enrollment Confirmed – Clarity Edge',
                #     f'Hi {first_name}, you are now enrolled in {course.subject_name}.',
                #     'noreply@clarityedge.in',
                #     [email],
                # )

            else:
                messages.info(request, "This user has already enrolled in this course")
                return redirect('/enrollment/') 
            
            return redirect('/home-page/')
    except ValueError:
        messages.info(request, "Please Fill the form first")
        return redirect('/enrollment/')

    print(enrollment_data.objects.values())
    courses = Course.objects.all()
    

    # if course_id in enrolled_course_ids:
    #     print('yes')


    return render(request, 'enrollment.html', {'courses' : courses})

def log_out(request):
    logout(request)
    return redirect('/student-login/')

@login_required(login_url='/student-login/')
def curriculum(request, id):
    students_enrolled = enrollment_data.objects.all()
    students_enrolled = len(students_enrolled)
    course = Course.objects.get(id=id)
    subject_enrolled = enrollment_data.objects.values_list('course', flat=True)
    # print(subject_enrolled)
    topic_link = topic_links.objects.get(id=1)   
    purchased_course_list = Order.objects.all()
    order_status = Order.objects.filter(user=request.user, course=course).first()                                                                                                                                           
    # print(purchased_course_list.values())
    
    price = course.price
    original_price = course.original_price
    discount = original_price - price
    discount_percentage = ( discount / original_price ) * 100
    discount_percentage = int(discount_percentage)

    watched_ids = VideoProgress.objects.filter(
        user=request.user,
        watched=True
    ).values_list('topic_link_id', flat=True)


    context = {"students_enrolled" : students_enrolled, 
               "course" : course, 
               "topic_link" : topic_link, 
               'purchased_course_list': purchased_course_list, 
               'order_status':order_status,
               'discount_percentage' : discount_percentage,
               'watched_ids': watched_ids
               }
    print(watched_ids)
    return render(request, 'curriculum.html', context)

@login_required(login_url='/student-login/')
def videos(request, topic_id):
    # topic_link = topic_links.objects.get(id=topic_id)
    # course = topic_link.topic.module.course

    # topic = get_object_or_404(Topic, topic_id)
    topic_link = topic_links.objects.get(id=topic_id)
    course = Course.objects.all()

    next = topic_links.objects.filter(id__gt = topic_id).order_by('id').first()
    prev = topic_links.objects.filter(id__lt = topic_id).order_by('-id').first()

    # check if previous video was watched
    if prev:
        prev_watched = VideoProgress.objects.filter(
            user=request.user,
            topic_link=prev,
            watched=True
        ).exists()
    else:
        prev_watched = True  # first video — no previous, always accessible

    if not prev_watched:
        return render(request, 'watch_previous.html', {
            'prev': prev,
            'course': course
        })
    
    # mark current video as watched when user opens it
    VideoProgress.objects.get_or_create(
        user=request.user,
        topic_link=topic_link,
        defaults={'watched': True}
    )


    total_topics = topic_links.objects.count()
    current_position = topic_links.objects.filter(id__lte=topic_id).count()
    progress = int((current_position / total_topics) * 100)


    Attendance.objects.create(
        present = 'present'
    )

    context = {
                "topic_link" : topic_link, 
                "course" : course, 
                'next' : next, 
                'prev' : prev, 
                "progress": progress,
                "current_position": current_position,
                "total_topics": total_topics
            }
    print(VideoProgress.objects.values())

    return render(request, 'videos.html', context)

@login_required(login_url='/student-login/')
def purchase(request, course_id):
    
    course = get_object_or_404(Course, id=course_id)
    
    amount = int(course.price * 100)  # ₹499 in paise

    razorpay_order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': 1
    }) 
    

    Order.objects.create(
        user=request.user,
        course=course,
        amount_paid = course.price,
        original_price = course.original_price,
        discount = (course.original_price) - (course.price),
        status='pending',
        razorpay_order_id = razorpay_order['id']
    )

    context = {
        'course': course,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount,
        'discount' : (course.original_price) - (course.price)
    }
    return render(request, 'purchase.html', context)

@login_required(login_url='/student-login/')
@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        }

        try:
            client.utility.verify_payment_signature(params)

            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.status = 'completed'
            order.save()

            # create enrollment so user can access the course
            user_n_course.objects.get_or_create(
                user=order.user,
                course=order.course,
            )
            print(Order.objects.values())
            return redirect('/payment/success/')

        except:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.status = 'failed'
            order.save()
            return redirect('/payment/failed/')


@login_required(login_url='/student-login/')
def payment_success(request):
    return render(request, 'payment_success.html')

@login_required(login_url='/student-login/')
def payment_failed(request):
    return render(request, 'payment_failed.html')

@login_required(login_url='/student-login/')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='/student-login/')
def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='/student-login/')
def profile(request):
    box = Attendance.objects.all()

    context = {
        'box' : box
        
    }
    return render(request, 'profile.html', context)