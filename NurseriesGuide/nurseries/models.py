from django.db import models
from django.contrib.auth.models import User
import re

# City Model
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Neighborhood Model
class Neighborhood(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='neighborhoods', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city.name},{self.name}"


# Nursery Model
class Nursery(models.Model):
    name = models.CharField(max_length=255)
    address = models.URLField(max_length=3000)  # Changed from CharField to URLField
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    accepts_special_needs = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='pending', choices=(
        ('pending', 'تحت المراجعه'),
        ('verified', 'موثق'),
        ('rejected', 'مرفوض')
    ))
    rejection_reason = models.TextField(blank=True, null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='nurseries')

    owner = models.ForeignKey(User, on_delete=models.CASCADE,  limit_choices_to={'is_staff': True})

    commercial_registry_file = models.FileField(upload_to='commercial_registry/', null=True, blank=True)
    license_file = models.FileField(upload_to='nursery_licenses/', null=True, blank=True)

    min_age = models.PositiveIntegerField(default=1)
    max_age = models.PositiveIntegerField(default=5)
    # max_age_unit = models.CharField(max_length=10, choices=(('months', 'أشهر'), ('years', 'سنوات')), default='years')
    # min_age_unit = models.CharField(max_length=10, choices=(('months', 'أشهر'), ('years', 'سنوات')), default='years')
    main_image = models.ImageField(upload_to='images/', default="images/nursery_default.jpg")

    def get_lat_lng(self):
        match = re.search(r'loc:([-\d.]+),([-\d.]+)', self.location)
        if match:
            return match.group(1), match.group(2)
        return None, None


    def __str__(self):
        return self.name



#Activity Model
class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    age_min = models.IntegerField(default=2)
    age_max = models.IntegerField(default=5)
    image = models.ImageField(upload_to='images/', default="images/default.jpg")
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


#Gallery Model
class Gallery(models.Model):
    image = models.ImageField(upload_to='images/', default="images/default.jpg")
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    nursery = models.ForeignKey('Nursery', on_delete=models.CASCADE)

#Staff Model
class Staff(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', default="images/profile_default.jpg")
    specializations = models.TextField()
    experience=models.TextField()
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
