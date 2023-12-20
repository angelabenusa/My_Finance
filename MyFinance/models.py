from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.forms import forms
from django.utils import timezone


# Create your models here.

class CategoryIncome(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('CategoryIncome', on_delete=models.CASCADE, related_name='income')
    date = models.DateField()

    def __str__(self):
        return self.category

class CategoryExpenses(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('CategoryExpenses', on_delete=models.CASCADE, related_name='expenses')
    date = models.DateField()

    def __str__(self):
        return self.category


WALLET_NAMES = (
    ('Main account', 'Main account'),
    ('Direct account', 'Direct account'),
    ('Savings Account', 'Savings Account'),
    ('Savings Account for a child', 'Savings Account for a child'),
    ('Saving goals', 'Saving goals'),
    ('Retirement', 'Retirement')
)
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expenses = models.ManyToManyField(Expenses)
    incomes = models.ManyToManyField(Income)
    name = models.CharField(max_length=255, choices=WALLET_NAMES, default='m')

    def __str__(self):
        return self.name



