from django.contrib import admin
from .models import  Staff, Student, Attendance,Course,ContactMessage


# ==========================================
# STAFF PANEL
# ==========================================
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staffid', 'name', 'contact')
    # Allows you to edit the contact number directly from the list!
    list_editable = ('contact',) 
    search_fields = ('staffid', 'name')

# ==========================================
# STUDENT PANEL
# ==========================================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # 'remaining' is calculated automatically, so we don't put it in list_editable
    list_display = ('std_id', 'name', 'course', 'timing', 'fees', 'fees_paid', 'remaining')
    
    # PRO FEATURE: Edit course, timing, and fees directly from the main table
    list_editable = ('course', 'timing', 'fees_paid') 
    
    list_filter = ('course', 'timing')
    search_fields = ('std_id', 'name', 'phone_number')

# ==========================================
# ATTENDANCE PANEL
# ==========================================
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'staff')
    
    # PRO FEATURE: Quickly change Absent to Present directly from the list
    list_editable = ('status',) 
    
    list_filter = ('date', 'status')
    search_fields = ('student__name', 'student__std_id')

admin.site.register(Course)
admin.site.register(ContactMessage)