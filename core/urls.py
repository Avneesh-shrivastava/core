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
from home.views import *
from vege.views import *
from enrollment.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from edu.views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-page/', about, name='about'),
    path('contact-page/', contact, name='contact'),
    path('receipes/' ,receipes,name='receipes'),
    path('students/', students, name='students'),
    path('admin/', admin.site.urls),
    path('delete-receipe/<id>/', delete_receipe, name='delete_receipe' ),
    path('update-receipe/<id>/', update_receipe, name='update_receipe'),
    path('student-login/', student_login, name='student_login'),
    path('student-signup/', student_signup, name='student_signup'),
    path('show-data/', show_data, name='show_data'),
    path('delete-data/<id>/', delete_data, name='delete_data'),
    path('home-page/', home_page, name='home_page'),
    path('course/', courses, name='courses'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()