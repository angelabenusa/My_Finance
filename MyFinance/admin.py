from django.contrib import admin
from MyFinance.models import CategoryIncome, Income, CategoryExpenses, Expenses, Wallet

# Register your models here.
admin.site.register(CategoryIncome)
admin.site.register(CategoryExpenses)
admin.site.register(Income)
admin.site.register(Expenses)
admin.site.register(Wallet)
