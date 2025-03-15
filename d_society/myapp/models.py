from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
9

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):  # ✅ Inherit from AbstractBaseUser
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
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # Use custom manager

    USERNAME_FIELD = "email"  
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
