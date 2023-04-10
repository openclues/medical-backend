from django.utils import timezone

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    is_banned = models.BooleanField(default=False, blank=True, null=True)
    addresses = models.ManyToManyField('Address', related_name='users')
    national_id = models.PositiveIntegerField(blank=True, null=True)
    profile_pic = models.FileField(upload_to="pics", blank=True, null=True)
    is_verified = models.BooleanField(default=False, blank=True, null=True)
    has_membership = models.BooleanField(default=False, null=True, blank=True)
    # Interested in which departments.


class Interest(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='interests')
    specialties = models.ManyToManyField('Specialty', related_name='interested_users')


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    billing_interval = models.CharField(max_length=255)
    billing_frequency = models.IntegerField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    trial_period = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is None:
            # This is a new subscription, so set start_date to the current date if it's not set already.
            if self.start_date is None:
                self.start_date = timezone.now().date()
            # Calculate the end date based on the plan's billing interval and frequency.
            if self.trial_period > 0:
                self.end_date = self.start_date + relativedelta(days=self.trial_period)
            elif self.plan.billing_interval == 'month':
                self.end_date = self.start_date + relativedelta(months=self.plan.billing_frequency)
            elif self.plan.billing_interval == 'year':
                self.end_date = self.start_date + relativedelta(years=self.plan.billing_frequency)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username + " Subscribed in " + self.plan.name + " until " + str(self.end_date)


class Transaction(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, blank=True, null=True)


class TeamMember(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    medical_center = models.ForeignKey('MedicalCenter', on_delete=models.CASCADE, related_name='team_members_list')
    is_moderator = models.BooleanField(default=False)


class Specialty(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='speciality', blank=True, null=True)

    def __str__(self):
        return self.name


class MedicalCenter(models.Model):
    admin = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='admin_of')
    team_members = models.ManyToManyField(UserAccount, related_name='team_member_centers')
    title = models.CharField(max_length=255)
    overview = models.TextField()
    phone = models.CharField(max_length=20)
    is_promoted = models.BooleanField(default=False, blank=True, null=True)
    email = models.EmailField()
    logo = models.ImageField(upload_to='logos', blank=True, null=True)
    url = models.URLField()
    cover = models.FileField(upload_to='covers', blank=True, null=True)
    #social media

    # Ratings

    def __str__(self):
        return self.title


class MedicalCenterSpecialty(models.Model):
    speciality = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="center_speciality", blank=True,
                                   null=True)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE,
                                       related_name='center_speciality_information')
    description = models.TextField(blank=True, null=True)
    offer = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.medical_center.title + " Speciality Information")


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_free = models.BooleanField(default=False, blank=True, null=True)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name="center_services")
    offer = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class CustomField(models.Model):
    FIELD_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('boolean', 'Boolean'),
    )
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPES)
    text_value = models.TextField(blank=True, null=True)
    image_value = models.ImageField(upload_to='custom_fields', blank=True, null=True)
    boolean_value = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='doctors', blank=True, null=True)
    specialist = models.ForeignKey(Specialty, blank=True, null=True, on_delete=models.SET_NULL)
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, related_name='doctors')
    experiences = models.PositiveIntegerField( blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    offer = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Address(models.Model):
    url = models.URLField(blank=True, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_province = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    branche_name = models.CharField(max_length=300, blank=True, null=True)
    medicalCenter = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name="addresses")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)


class Favorite(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="favorites")
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'medical_center')

# General user
# national id just numbers max 15

##Download create account , national Id, Islam,
##activation mobile.
## personal / Family description // first, second. expiered after 1 year
##Browser the centers. //blur the list.
##coupons
##Sawany
##


# scanner
# user information.
# user subscription information.
