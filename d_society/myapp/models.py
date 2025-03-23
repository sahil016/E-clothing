from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models    

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('chairman', 'Chairman'),
        ('member', 'Member'),
        ('visitor', 'Visitor'),
        ('watchman', 'Watchman'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    
    is_active = models.BooleanField(default=False)

   
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username



# Chairman Model
class Chairman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chairman_profile')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Allow blank values

    def __str__(self):
        return f"Chairman: {self.user.username}"

# Member Model
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    house_no = models.CharField(max_length=10)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Member: {self.user.username}"

# Visitor Model (Fixed Typo)
class Visitor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    visit_date = models.DateTimeField(auto_now_add=True)  # Fixed typo
    purpose = models.TextField()

    def __str__(self):
        return f"Visitor: {self.name}"

# Watchman Model
class Watchman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchman_profile')
    shift = models.CharField(max_length=20, choices=[('day', 'Day'), ('night', 'Night')], default='day')

    def __str__(self):
        return f"Watchman: {self.user.username}"

class Notice(models.Model):
    title = models.CharField(max_length=200)  # Title of the notice
    content = models.TextField()  # Content of the notice
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the notice was created

    def __str__(self):
        return self.title
    
class Event(models.Model):
    title = models.CharField(max_length=200)  # Title of the event
    description = models.TextField()  # Description of the event
    event_date = models.DateTimeField()  # Date and time of the event
    location = models.CharField(max_length=255)  # Location of the event
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the event was created
    
    def __str__(self):
        return self.title