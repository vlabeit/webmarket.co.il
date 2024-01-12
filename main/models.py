from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    #user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=55, blank=True)
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    message = models.CharField(max_length=100)
    phone = PhoneNumberField()

    class Meta:
        verbose_name_plural = "Contact Us"
    
    def __str__(self):
        return self.title