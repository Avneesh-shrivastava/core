"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from edu.views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('admin/', admin.site.urls),
    path('student-login/', student_login, name='student_login'),
    path('student-signup/', student_signup, name='student_signup'),
    path('show-data/', show_data, name='show_data'),
    path('delete-data/<id>/', delete_data, name='delete_data'),
    path('home-page/', home_page, name='home_page'),
    path('course/', courses, name='courses'),
    path('search-results/', search_results , name='search_results'),
    path('enrollment/', enrollment_form, name='enrollment_form'),
    path('logout', log_out, name='logout'),
    path('curriculum/<int:id>/', curriculum, name='curriculum'),
    path('videos/<int:topic_id>',videos,name='videos'),
    path('purchase/<int:course_id>/', purchase, name='purchase'),
    path('payment/verify/', verify_payment, name='verify_payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failed/', payment_failed, name='payment_failed'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()