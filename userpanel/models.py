from django.shortcuts import get_object_or_404
from simple_history.models import HistoricalRecords
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.db import models
from users.models import CustomUser
from django.urls import reverse
from oscar.apps.catalogue.models import Product as addon_product

class Choicesprod(models.Model):  # change later to product table model
    #project = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True, blank=True)
    choice = models.CharField(
        max_length=100, blank=True, default='אתר תדמית')

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name_plural = "Project Categories"

def day_365():
    return timezone.now() + timezone.timedelta(days=365)

def day_30():
    return timezone.now() + timezone.timedelta(days=30)

class BackupPlans(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    price_monthly = models.DecimalField(max_digits=7, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=7, decimal_places=2)
    details = models.TextField(max_length=255, blank=True)
    type = models.CharField(max_length=100, default='web') # web/system

    def __str__(self):
        return f"{self.name} {self.company} - {self.price_monthly} {self.price_yearly}"


class SupportPlans(models.Model):
    name = models.CharField(max_length=100)  # will be foreign key
    company = models.CharField(max_length=100)
    price_monthly = models.DecimalField(max_digits=7, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=7, decimal_places=2)
    details = models.TextField(max_length=255, blank=True)
    type = models.CharField(max_length=100, default='web') # web/system

    def __str__(self):
        return str(f"{self.name} - {self.price_monthly}")


class UserSupport(models.Model):
    plan = models.ForeignKey(SupportPlans, on_delete=models.SET_NULL, blank=True, null=True)
    plan_name = models.CharField(max_length=100, blank=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    PERIOD_CHOICES = (
        ('monthly', 'Monthly',),
        ('yearly', 'Yearly',),
    )
    period = models.CharField(
        max_length=7,
        choices=PERIOD_CHOICES,
    )
    # period = models.CharField(max_length=20, default='monthly', blank=True)
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    end_time = models.DateTimeField(default=timezone.now)
    next_payment = models.DateTimeField(default=timezone.now) # change every payment to next payment (monthly/yearly)
    last_payment = models.DateTimeField(default=timezone.now) # add on every payment
    type = models.CharField(max_length=100, default='web', blank=True)
    kind = 'support'


    def __str__(self):
        return str(self.user_id)

    # def __init__(self, *args, **kwargs):
    #     self.kind = 'support'

    def save(self, silent=False, *args, **kwargs):
        if not silent and not self.pk:
            self.plan_name = SupportPlans.objects.get(id=self.plan_id).name
            self.type = SupportPlans.objects.get(id=self.plan_id).type
            self.end_time = day_365()
            # estimate finish date by project category
            inst = get_object_or_404(SupportPlans, id=self.plan_id)
            if self.period == 'monthly':
                self.end_time = day_30()
                self.price = inst.price_monthly
            else:
                self.end_time = day_365()
                self.price = inst.price_yearly
            if self.is_active and self.period == 'monthly':
                self.next_payment = day_30()
                self.price = inst.price_monthly
            elif self.is_active and self.period == 'yearly':
                self.next_payment = day_365()
                self.price = inst.price_yearly
        return super(UserSupport, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('users:userpanel:project-detail', kwargs={'pk': self.pk})
















class StoragePlans(models.Model):
    name = models.CharField(max_length=100)  # will be foreign key
    company = models.CharField(max_length=100)
    price_monthly = models.DecimalField(max_digits=7, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=7, decimal_places=2)
    details = models.TextField(max_length=255, blank=True)
    type = models.CharField(max_length=100, default='web') # web/system

    def __str__(self):
        return str(f"{self.name} - {self.price_monthly}")


class UserStorage(models.Model):
    plan = models.ForeignKey(StoragePlans, on_delete=models.SET_NULL, blank=True, null=True)
    plan_name = models.CharField(max_length=100, blank=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    PERIOD_CHOICES = (
        ('monthly', 'Monthly',),
        ('yearly', 'Yearly',),
    )
    period = models.CharField(
        max_length=7,
        choices=PERIOD_CHOICES,
    )
    # period = models.CharField(max_length=20, default='monthly', blank=True)
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    end_time = models.DateTimeField(default=timezone.now)
    next_payment = models.DateTimeField(default=timezone.now) # change every payment to next payment (monthly/yearly)
    last_payment = models.DateTimeField(default=timezone.now) # add on every payment
    type = models.CharField(max_length=100, default='web', blank=True)
    kind = 'storage'

    def __str__(self):
        return str(self.user_id)

    # def __init__(self, *args, **kwargs):
    #     self.kind = 'support'

    def save(self, silent=False, *args, **kwargs):
        if not silent and not self.pk:
            self.plan_name = StoragePlans.objects.get(id=self.plan_id).name
            self.type = StoragePlans.objects.get(id=self.plan_id).type
            self.end_time = day_365()
            # estimate finish date by project category
            inst = get_object_or_404(StoragePlans, id=self.plan_id)
            if self.period == 'monthly':
                self.end_time = day_30()
                self.price = inst.price_monthly
            else:
                self.end_time = day_365()
                self.price = inst.price_yearly
            if self.is_active and self.period == 'monthly':
                self.next_payment = day_30()
                self.price = inst.price_monthly
            elif self.is_active and self.period == 'yearly':
                self.next_payment = day_365()
                self.price = inst.price_yearly
        return super(UserStorage, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('users:userpanel:project-detail', kwargs={'pk': self.pk})






class SecurityProducts(models.Model):
    name = models.CharField(max_length=100)  # will be foreign key
    company = models.CharField(max_length=100, default='webmarket')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    details = models.TextField(max_length=255, blank=True)
    type = models.CharField(max_length=100, default='web') # web/system
    product_url = models.URLField(max_length=100, blank=True)

    def __str__(self):
        return str(f"{self.name} - {self.price}")


class UserSecurity(models.Model):
    plan = models.ForeignKey(SecurityProducts, on_delete=models.SET_NULL, blank=True, null=True)
    plan_name = models.CharField(max_length=100, blank=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    type = models.CharField(max_length=100, default='web', blank=True)


    def __str__(self):
        return str(self.plan_name)

    def save(self, silent=False, *args, **kwargs):
        if not silent and not self.pk:
            self.plan_name = SecurityProducts.objects.get(id=self.plan_id).name
            self.type = SecurityProducts.objects.get(id=self.plan_id).type
            self.price = get_object_or_404(SecurityProducts, id=self.plan_id).price
        return super(UserSecurity, self).save(*args, **kwargs)










class Projects(models.Model):
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    user_email = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    project_name = models.CharField(max_length=30)
    project_category = models.ForeignKey(
        Choicesprod, on_delete=models.SET_NULL, blank=True, null=True)
    date_started = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30, default='accepted')
    site_category = models.CharField(max_length=30, blank=True)
    main_languages = models.CharField(max_length=30, blank=True)
    est_finish = models.DateTimeField(blank=True, null=True)
    project_percent = models.CharField(max_length=30, blank=True, default='5')
    history = HistoricalRecords()
    content = RichTextField(blank=True, null=True,
        default='אנא מלא תוכן אתר לדף הראשי ודפים נוספים')
    content_upload = models.FileField(
        upload_to='media/', null=True, blank=True)
    is_install = models.BooleanField(default=False)
    storage_plan = models.ForeignKey(UserStorage, on_delete=models.SET_NULL, null=True, blank=True)
    support_plan = models.ForeignKey(UserSupport, on_delete=models.SET_NULL, null=True, blank=True)


    install = models.CharField(max_length=30, default='no_install')
    add_languages = models.CharField(max_length=30, blank=True)
    
    storage_active = models.BooleanField(default=False)
    support_active = models.BooleanField(default=False)
    
    add_ons = models.CharField(max_length=30, blank=True)

    slug = models.SlugField(blank=True)
    

    def save(self, silent=False, *args, **kwargs):
        # Copy email address to backup incase user delete.
        if not silent and not self.pk:
            self.user_email = self.user_id
            # estimate finish date by project category
            if self.project_category == 'second':
                self.est_finish = '312323'
        return super(Projects, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:userpanel:project-detail', kwargs={'pk': self.pk})

    # def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.user_email = self.user_id

    # def get_context_data(self, **kwargs):
    #        context = super().get_context_data(**kwargs)
    #        #context['usereal'] = CustomUser.objects.get(email= self.user_email)
    #        return context

    def __str__(self):
        return str(self.project_name)


class Menu(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    project_name = Projects.project_name
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SitePages(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Storage(models.Model):
    project = models.ForeignKey(
        Projects, on_delete=models.SET_NULL, null=True, blank=True)
    # project_ide = models.CharField(max_length=100) #copy of id incase project deleted
    plan = models.CharField(max_length=100)  # will be foreign key
    start_time = models.DateTimeField(default=timezone.now)
    period = models.CharField(max_length=10, default='yearly')
    end_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.plan


class Backup(models.Model):
    #project = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True, blank=True)
    # project_ide = models.CharField(max_length=100) #copy of id incase project deleted
    plan = models.CharField(max_length=100)  # will be foreign key
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.plan

class AddOns(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(addon_product, on_delete=models.SET_NULL, null=True, blank=True)
    projects = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=100)
    addon_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name



class ImageUploader(models.Model):
        image_name = models.CharField(max_length=100)
        image = models.ImageField(upload_to='Images')
        user = models.CharField(max_length=100) 
        user_profile = models.CharField(max_length=100)
        date = models.DateField()