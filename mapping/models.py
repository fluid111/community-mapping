from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager, BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Always run migrate after makemigrations
# When adding new models:
# Create the model
# makemigrations
# migrate
# Then add fields/relationships

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    email= models.EmailField(max_length=254,
                             unique=True,
                             error_messages={
            'unique': _("A user with that email already exists."),
        })
    # profile_picture = models.ImageField(upload_to='profile_pics/',height_field=None, width_field=None,max_length=100, blank = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()   # Explicitly declare the manager
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

class Park(models.Model):
    name = models.CharField(max_length=100, help_text="Official name of the park", blank=True)
    description = models.TextField(blank=True)
    latitude = models.FloatField(help_text="Geographic latitude in decimal degrees")
    longitude = models.FloatField(help_text="Geographic longitude in decimal degrees")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'parks'

    def __str__(self):
        return self.name

class ParkDescription(models.Model):
    name = models.OneToOneField(Park, on_delete= models.CASCADE , primary_key=True)
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True, help_text="Full address of the park")
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='park_images/', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Description for {self.name}"


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='submissions')
    place = models.ForeignKey(Park, on_delete=models.CASCADE,related_name='submissions')
    note = models.TextField(help_text="User's comments about the park")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(
        default=False,
        help_text="Moderation status"
    )

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'submissions'

    def __str__(self):
        return f"Submission by {self.user.email} for {self.place.name}"