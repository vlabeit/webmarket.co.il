from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from PIL import Image
from django.conf import settings
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

from storages.backends.s3boto3 import S3Boto3Storage

User = settings.AUTH_USER_MODEL


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='profile_pics/default.jpg', upload_to='profile_pics')
    city = models.CharField(max_length=25, blank=True)
    street = models.CharField(max_length=25, blank=True)
    apart = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    zipcode = models.CharField(max_length=25, blank=True, null=True)
    # phone = models.

    def __str__(self):
        return f'{self.user.email} Profile'


'''
class PhoneModel(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list

'''


class CustomUser(AbstractUser):
    age = models.PositiveBigIntegerField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=50, verbose_name="email", unique=True)
    REQUIRED_FIELDS = ['username']
    username = models.CharField(max_length=12, blank=True)
    ip_address = models.CharField(max_length=100, default='ipDefault')
    # is_sub = models.BooleanField(default=True)
    phone_regex = RegexValidator(
        regex=r'^\+?972?\d{2,14}$', message="Phone number must be in the format: '+xxxxxxxxxx'.")
    # phone = models.CharField(
    #     validators=[phone_regex], max_length=15, unique=False, blank=True)
    is_active = models.BooleanField(default=True)
    phone_numbers = PhoneNumberField()

    def __str__(self):
        return self.email

    def get_fullname(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name


class GuestIP(models.Model):
    user_id = models.CharField(max_length=50, unique=False)
    #ip_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=False)
    user_ip_address = models.CharField(
        max_length=100, default='ipDefault', unique=False)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_ip_address


def get_total(self):
    unique_list = []
    iplist = list(GuestIP.objects.distinct().values('user_ip_address'))
    for ip in iplist:
        for key in ip.values():
            if key not in unique_list:
                unique_list.append(key)
    total_visitors = len(unique_list)
    return f"{total_visitors} total visited site"


class UserAgent(models.Model):
    user_id = models.CharField(max_length=50, unique=False)
    user_ip_address = models.CharField(
        max_length=100, default='ipDefault', unique=False)
    time = models.DateTimeField(default=timezone.now)
    browser = models.CharField(max_length=100, blank=True, unique=False)
    broswer_id = models.CharField(max_length=100, blank=True, unique=False)
    os = models.CharField(max_length=100, blank=True, unique=False)
    os_id = models.CharField(max_length=100, blank=True, unique=False)
    device = models.CharField(max_length=100, blank=True, unique=False)
    device_brand = models.CharField(
        max_length=100, blank=True, unique=False, null=True)
    device_model = models.CharField(
        max_length=100, blank=True, unique=False, null=True)
    location = models.CharField(max_length=100, blank=True, unique=False)

    def __str__(self):
        return self.user_ip_address


'''
class CustomLoginView(LoginView):
    authentication_form = HeAuthForm
'''
