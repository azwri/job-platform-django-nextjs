from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
import geocoder
import os


def return_time():
    return (datetime.now() + timedelta(days=10))


class JobType(models.TextChoices):
    PERMANENT = 'Permanent'
    TEMPORARY = 'Temporary'
    INTERNSHIP = 'Internship'

class Education(models.TextChoices):
    BACHELORS = 'Bachelors'
    MASTERS = 'Masters'
    PHD = 'PhD'

class Industry(models.TextChoices):
    BUSINESS = 'Business'
    IT = 'IT'
    BANKING = 'Banking'
    EDUCATION = 'Education'
    TELECOM = 'Telecom'
    OTHER = 'Other'

class Experience(models.TextChoices):
    NO_EXPERIENCE = 'No Experience'
    ONE_YEAR = '1 Year'
    TWO_YEARS = '2 Years'
    THREE_YEARS_PLUS = '3 Years Plus'


class Job(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    job_type = models.CharField(max_length=30, choices=JobType.choices, default=JobType.PERMANENT)
    education = models.CharField(max_length=30, choices=Education.choices, default=Education.BACHELORS)
    industry = models.CharField(max_length=30, choices=Industry.choices, default=Industry.BUSINESS)
    experience = models.CharField(max_length=30, choices=Experience.choices, default=Experience.NO_EXPERIENCE)
    salary = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    position = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    company = models.CharField(max_length=100, null=True, blank=True)
    point = gis_models.PointField(default=Point(0, 0))
    last_date = models.DateTimeField(default=return_time)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        # Get the location from the address
        g = geocoder.mapquest(self.address, key=os.environ['GEOCODER_API'])
        print(g)
        if g.ok:
            # Update the point field with the new coordinates
            self.point = Point(g.lng, g.lat)
            print(self.point)
        super(Job, self).save(*args, **kwargs)
    
