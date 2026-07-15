from django.contrib import admin

# Register your models here.

from .models import Course, Module, Topic, Order, enrollment_data, user_n_course, topic_links

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Topic)
admin.site.register(Order)
admin.site.register(enrollment_data)
admin.site.register(user_n_course)
admin.site.register(topic_links)
