from django.db import models
from django.contrib.auth.models import User

FOUNDATION = 0
NON_GOV = 1
LOCAL_COLLECTION = 2

INSTYTUTION_CHOICE = {
    (FOUNDATION, "Fundacja"),
    (NON_GOV, "Organizacja pozarządowa"),
    (LOCAL_COLLECTION, "Zbiórka lokalna")
}


class Categoty(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    institution_type = models.SmallIntegerField(choices=INSTYTUTION_CHOICE, default=FOUNDATION)
    categories = models.ManyToManyField(Categoty)


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Categoty)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_comment = models.TextField()
    user = models.OneToOneField(User, null=True, default=None, on_delete=models.CASCADE)