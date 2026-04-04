from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Main Navigation
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('contact/', views.contact, name='contact'),
    path('course/',views.courses,name="couse"), 
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    
    # Staff Routes (Notice we split the view and the validation here just like you asked!)
    path('login/staff/', views.stf_login, name='staff_login'),
    path('login/staff-val/', views.staff_login, name='staff_login_val'),
    path('login/staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('logout/staff/', views.staff_logout, name='staff_logout'),
    path('staff/take-attendance/<str:course_name>/', views.take_attendance, name='take_attendance'),
    # Student Routes
    path('staff/attendance-history/', views.staff_attendance_report, name='staff_attendance_report'),

    path('login/student/', views.student_login, name='student_login'),
    path('login/student-dashboard/', views.student_dashboard, name='student_dashboard'),
    #path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    # ... inside your Student Routes section ...
    path('logout/student/logout', views.student_logout, name='student_logout'),
    #path('logout/student/', views.student_logout, name='student_logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)