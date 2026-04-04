from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# ==========================================
# 2. STAFF MODEL
# ==========================================
class Staff(models.Model):
    staffid = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=15)
    Qualification = models.CharField(max_length=100, null=True, blank=True) # <-- ADD THESE

    def save(self, *args, **kwargs):
        # Securely hash the password before saving
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.staffid})"


# ==========================================
# 3. STUDENT MODEL
# ==========================================
class Student(models.Model):
    std_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    timing = models.CharField(max_length=50) 
    assigned_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_students')
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remaining = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    marks = models.IntegerField(default=0, blank=True, null=True)

    # --- Dynamic Attendance Properties ---
    @property
    def total_classes(self):
        return self.attendance_records.count()

    @property
    def days_present(self):
        return self.attendance_records.filter(status='Present').count()

    @property
    def attendance_percentage(self):
        total = self.total_classes
        if total == 0:
            return 0 
        return round((self.days_present / total) * 100, 2)

    # --- Save & Verification Methods ---
    def save(self, *args, **kwargs):
        # Auto-calculate remaining fees
        if self.fees is not None and self.fees_paid is not None:
            self.remaining = self.fees - self.fees_paid
            
        # Securely hash the password
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
            
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.std_id})"


# ==========================================
# 4. ATTENDANCE MODEL
# ==========================================
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    )

    # Linked to Student (This creates the 'attendance_records' connection used in the @properties above)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    
    # Linked to Staff marking the attendance
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='course_images/')
    duration = models.CharField(max_length=50) # e.g., "3 Months", "6 Months"
    content = models.TextField() # Allows for long descriptions of the syllabus

    def __str__(self):
        return self.name
    
# Add this at the bottom of models.py
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.CharField(max_length=100, blank=True, null=True) # Optional field
    feedback = models.TextField() # This will store their message
    submitted_at = models.DateTimeField(auto_now_add=True) # Automatically saves the exact date and time

    def __str__(self):
        return f"Inquiry from {self.name} - {self.course}"