from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Staff,Student,Attendance # Import the Staff model
from django.utils import timezone
def home(request):
    # Context dictionary passing dynamic data to the frontend
    context = {
        'main_heading': 'CSC COMPUTER EDUCATION',
        'sub_heading': 'BOON FOR MIDDLE CLASS',
        'founder_name': 'Mr. T. Iyamperumal M.E',
        'branch_count': '400+'
    }
    return render(request, 'index.html', context)

from .models import Staff, Student, Attendance, Course, ContactMessage

def about(request):
    # Fetch all courses to display in the new section on the About page
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses
    }
    return render(request, 'about.html', context)
def courses(request):
    # You can later fetch your course list (HTML, Python, Java, Full Stack) from the database here
    return render(request, 'courses.html')

def contact(request):
    return render(request, 'contact.html')

# --- Login Views ---

def student_login(request):
    return render(request, 'stdlogin.html')
# 1. View just to SHOW the login page
def stf_login(request):
    # Make sure this points to your actual HTML file path!
    return render(request, 'stflogin.html')

# 2. View just to VALIDATE the data
def staff_login(request):
    if request.method == 'POST':
        input_userid = request.POST.get('userid')
        input_password = request.POST.get('password')

        try:
            staff = Staff.objects.get(staffid=input_userid)
            
            if staff.verify_password(input_password):
                # SUCCESS: Create session and go to dashboard
                request.session['staff_logged_in'] = True
                request.session['staff_id'] = staff.staffid
                
                return redirect('staff_dashboard') 
            else:
                # FAIL: Wrong password
                messages.error(request, "Invalid password. Please try again.")
                return redirect('staff_login') # Send them back to the login page
                
        except Staff.DoesNotExist:
            # FAIL: Wrong ID
            messages.error(request, "Staff ID not found.")
            return redirect('staff_login') # Send them back to the login page

    # If someone tries to visit the validation URL directly without submitting a form, kick them back
    return redirect('staff_login')
def staff_dashboard(request):
    if not request.session.get('staff_logged_in'):
        messages.warning(request, "Access Denied. You must log in first.")
        return redirect('staff_login')
        
    current_staff = Staff.objects.get(staffid=request.session['staff_id'])
    
    # NEW: Find all unique courses for students assigned to THIS specific staff member
    assigned_courses = Student.objects.filter(assigned_staff=current_staff).values_list('course', flat=True).distinct()
    
    context = {
        'staff': current_staff,
        'courses': assigned_courses # Pass the courses to the HTML
    }
    return render(request, 'staff_dashboard.html', context)


# NEW VIEW: To handle the actual attendance marking
def take_attendance(request, course_name):
    if not request.session.get('staff_logged_in'):
        return redirect('staff_login')

    current_staff = Staff.objects.get(staffid=request.session['staff_id'])
    
    # Get all students assigned to this staff member FOR THIS SPECIFIC COURSE
    students = Student.objects.filter(assigned_staff=current_staff, course=course_name)

    if request.method == 'POST':
        # Get the date from the form (defaults to today)
        date = request.POST.get('attendance_date', timezone.now().date())
        
        # Loop through submitted form data to save attendance
        for student in students:
            # The HTML form will send data named like 'status_STD001'
            status = request.POST.get(f'status_{student.std_id}')
            if status:
                # update_or_create ensures we don't create double records if they submit twice in one day
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'staff': current_staff, 'status': status}
                )
        messages.success(request, f"Attendance successfully saved for {course_name}!")
        return redirect('staff_dashboard')

    context = {
        'staff': current_staff,
        'course_name': course_name,
        'students': students,
        'today': timezone.now().strftime('%Y-%m-%d')
    }
    return render(request,'take_attendence.html', context)


def staff_logout(request):
    # Safely delete the session data
    if 'staff_logged_in' in request.session:
        del request.session['staff_logged_in']
        del request.session['staff_id']
    
    messages.success(request, "You have been successfully logged out.")
    return render(request,'index.html') # Send them back to the main website

def attendance_report(request):
    all_students = Student.objects.all()
    context = {'students': all_students}
    return render(request, 'attendance_report.html', context)

def student_login(request):
    # 1. VALIDATION: If the student clicks the submit button (POST request)
    if request.method == 'POST':
        input_userid = request.POST.get('userid')
        input_password = request.POST.get('password')

        try:
            # Look for the Student in the database using std_id
            student = Student.objects.get(std_id=input_userid)
            
            # Verify the hashed password
            if student.verify_password(input_password):
                # SUCCESS: Create secure session variables
                request.session['student_logged_in'] = True
                request.session['student_id'] = student.std_id
                
                # Send them to the dashboard you just built!
                return redirect('student_dashboard') 
            else:
                # FAILED: Wrong password
                messages.error(request, "Invalid password. Please try again.")
                return redirect('student_login')
                
        except Student.DoesNotExist:
            # FAILED: Student ID doesn't exist
            messages.error(request, "Student ID not found. Please check your ID.")
            return redirect('student_login')

    # 2. VIEW: If they are just visiting the page normally (GET request)
    # Make sure 'login/student_login.html' is the correct path to your HTML file
    return render(request, 'stdlogin.html')


def student_dashboard(request):
    # Security check: Kick them back to login if they don't have a session
    if not request.session.get('student_logged_in'):
        return redirect('student_login')
        
    # Fetch the specific student's full data from the database
    current_student = Student.objects.get(std_id=request.session['student_id'])
    
    context = {
        'student': current_student
    }
    return render(request, 'student_dashboard.html', context)

def student_logout(request):
    # Check if the student session exists, and safely delete it
    if 'student_logged_in' in request.session:
        del request.session['student_logged_in']
        del request.session['student_id']
    
    # Show a nice popup on the home page confirming they logged out
    messages.success(request, "You have been successfully logged out.")
    
    # Send them back to the main website
    return redirect('home')

from .models import Staff, Student, Attendance, Course # Import Course at the top

# Update your courses view:
def courses(request):
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses
    }
    return render(request, 'courses.html', context)

from .models import Staff, Student, Attendance, Course, ContactMessage # <-- Import it here

# Replace your current contact view with this:
def contact(request):
    if request.method == 'POST':
        # 1. Grab all the data from the HTML form
        input_name = request.POST.get('name')
        input_email = request.POST.get('email')
        input_phone = request.POST.get('phone')
        input_course = request.POST.get('course')
        input_message = request.POST.get('message') # From the textarea
        
        # 2. Save it securely to the database
        ContactMessage.objects.create(
            name=input_name,
            email=input_email,
            phone=input_phone,
            course=input_course,
            feedback=input_message
        )
        
        # 3. Show the success popup
        messages.success(request, f"Thank you, {input_name}! Your message has been saved and our team will contact you shortly.")
        
        return redirect('contact')

    return render(request, 'contact.html')

def staff_attendance_report(request):
    # Security check
    if not request.session.get('staff_logged_in'):
        return redirect('staff_login')
        
    current_staff = Staff.objects.get(staffid=request.session['staff_id'])
    
    # Fetch all attendance records marked by this specific staff member
    # .order_by('-date') makes sure the newest records show up at the very top!
    records = Attendance.objects.filter(staff=current_staff).select_related('student').order_by('-date')
    
    context = {
        'staff': current_staff,
        'records': records
    }
    return render(request, 'staff_attendance_report.html', context)