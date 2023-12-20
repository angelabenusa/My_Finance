from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import request

from MyFinance.models import Income, CategoryIncome, Expenses, CategoryExpenses, Wallet


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        data = super().clean()
        password = data['password']
        password2 = data['password2']
        if password != password2:
            raise ValidationError('Hasła nie są takie same')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CategoryIncomeForm(forms.ModelForm):
    class Meta:
        model = CategoryIncome
        fields = ['name']


class IncomeForm(forms.ModelForm):
    date = forms.DateField(
        label='Wybierz datę',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Income
        fields = ['value', 'category', 'date']

    def save(self, commit=True):
        income = super(IncomeForm, self).save(commit=False)
        if commit:
            income.save()
        return income


class IncomeWalletForm(forms.ModelForm):
    wallet = forms.ModelChoiceField(queryset=Wallet.objects.all(), label='Portfel', required=True)
    date = forms.DateField(
        label='Wybierz datę',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Income
        fields = ['value', 'category', 'date']

    def save(self, commit=True):
        income = super(IncomeWalletForm, self).save(commit=False)
        if commit:
            income.save()
        return income


class ExpensesWalletForm(forms.ModelForm):
    wallet = forms.ModelChoiceField(queryset=Wallet.objects.all(), label='Portfel', required=True)
    date = forms.DateField(
        label='Wybierz datę',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Expenses
        fields = ['value', 'category', 'date']

    def save(self, commit=True):
        expenses = super(ExpensesWalletForm, self).save(commit=False)
        if commit:
            expenses.save()
        return expenses


class CategoryExpensesForm(forms.ModelForm):
    class Meta:
        model = CategoryExpenses
        fields = ['name']


class ExpensesForm(forms.ModelForm):
    date = forms.DateField(
        label='Wybierz datę',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Expenses
        fields = ['value', 'category', 'date']

    def save(self, commit=True):
        expenses = super(ExpensesForm, self).save(commit=False)
        if commit:
            expenses.save()
        return expenses


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class FilterExpensesForm(forms.Form):
    date_from = forms.DateField(
        label='Wybierz datę od',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    date_to = forms.DateField(
        label='Wybierz datę do',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    value_from = forms.DecimalField(label='Wartość od', required=False)
    value_to = forms.DecimalField(label='Wartość do', required=False)
    category = forms.ModelChoiceField(queryset=CategoryExpenses.objects.all(), label='Kategoria', required=False)


class FilterIncomeForm(forms.Form):
    date_from = forms.DateField(
        label='Wybierz datę od',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    date_to = forms.DateField(
        label='Wybierz datę do',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    value_from = forms.DecimalField(label='Wartość od', required=False)
    value_to = forms.DecimalField(label='Wartość do', required=False)
    category = forms.ModelChoiceField(queryset=CategoryIncome.objects.all(), label='Kategoria', required=False)


class AddWalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name']

class TransfersForm(forms.Form):

    source_wallet = forms.ModelChoiceField(queryset=Wallet.objects.all(), label='Nazwa portfela', required=True)
    destination_wallet = forms.ModelChoiceField(queryset=Wallet.objects.all(), label='Nazwa portfela', required=True)
    value = forms.DecimalField(label='Wartość', required=True)
    date = forms.DateField(
        label='Wybierz datę',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False)

