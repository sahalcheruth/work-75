
from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}"

class Company(models.Model):
    name = models.CharField(max_length=100)
    catchPhrase = models.CharField(max_length=200)
    bs = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    website = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
