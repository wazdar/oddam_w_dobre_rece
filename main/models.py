from django.db import models
from django.contrib.auth.models import User

FOUNDATION = 0
NON_GOV = 1
LOCAL_COLLECTION = 2

INSTITUTION_CHOICE = {
    (FOUNDATION, "Fundacja"),
    (NON_GOV, "Organizacja pozarządowa"),
    (LOCAL_COLLECTION, "Zbiórka lokalna")
}


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    institution_type = models.SmallIntegerField(choices=INSTITUTION_CHOICE, default=FOUNDATION)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    class Meta:
        ordering = ['pick_up_date']

    def __str__(self):
        return f'{self.quantity} dla {self.institution.name} od {self.user.first_name} {self.user.last_name}'

    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)
