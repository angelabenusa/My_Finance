from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from MyFinance.forms import ContactForm, IncomeForm, CategoryIncomeForm, \
    LoginForm, UserCreateForm, CategoryExpensesForm, ExpensesForm, FilterExpensesForm, FilterIncomeForm, AddWalletForm, \
    IncomeWalletForm, ExpensesWalletForm
from MyFinance.models import CategoryIncome, Income, Expenses, CategoryExpenses, Wallet


# Create your views here.
#


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form_generic.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'wallets')
                return redirect(next_url)
            form = LoginForm()
        return render(request, 'form_generic.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('wallets')


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'form_generic.html'
    success_url = reverse_lazy('login')


class HomePageAccountBalanseView(LoginRequiredMixin, View):
    template_name = "homepage_with_account_balance.html"

    def get(self, request):
        income = Income.objects.filter(user=request.user)
        suma = 0
        for i in income:
            suma += i.value

        context = {
            'total_income': suma
        }
        return render(request, self.template_name, context)


class AddCategoryIncomeView(LoginRequiredMixin, View):
    template_name = 'add_category_income.html'

    def get(self, request):
        form = CategoryIncomeForm()  # creating empty form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryIncomeForm(request.POST)
        if form.is_valid():
            current_user = request.user

            new_category = form.save(commit=False)  # saving new category to database
            new_category.user = current_user
            new_category.save()
            return redirect('category_income_list')
        return render(request, self.template_name, {'form': form})


class CategoryIncomeListView(LoginRequiredMixin, View):
    template_name = 'category_income_list.html'

    def get(self, request):
        form = CategoryIncomeForm()
        categories = CategoryIncome.objects.filter(
            user=request.user)  # storing all existing income categories from database in this variable
        return render(request, self.template_name, {'categories': categories, 'form': form})

    def post(self, request):
        form = CategoryIncomeForm(request.POST)
        if form.is_valid():
            user = request.user
            categories = form.save(commit=False)
            categories.user = user
            categories.save()
            return redirect('category_income_list')
        return redirect(request, self.template_name, {'form': form})


class EditCategoryIncomeListView(LoginRequiredMixin, UpdateView):
    model = CategoryIncome
    fields = ['name']
    template_name = 'edit_form.html'
    success_url = reverse_lazy('category_income_list')


class EditCategoryExpensesListView(LoginRequiredMixin, UpdateView):
    model = CategoryExpenses
    fields = ['name']
    template_name = 'edit_form.html'
    success_url = reverse_lazy('category_expenses_list')


class DeleteCategoryIncomeListView(LoginRequiredMixin, DeleteView):
    model = CategoryIncome
    template_name = 'delete_form.html'
    success_url = reverse_lazy('category_income_list')


class DeleteCategoryExpensesListView(LoginRequiredMixin, DeleteView):
    model = CategoryExpenses
    template_name = 'delete_form.html'
    success_url = reverse_lazy('category_expenses_list')



class AddCategoryExpensesView(LoginRequiredMixin, View):
    template_name = 'add_category_expenses.html'

    def get(self, request):
        form = CategoryExpensesForm()  # creating empty form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryExpensesForm(request.POST)
        if form.is_valid():
            current_user = request.user

            new_category = form.save(commit=False)  # saving new category to database
            new_category.user = current_user
            new_category.save()
            return redirect('category_expenses_list')
        return render(request, self.template_name, {'form': form})


class CategoryExpensesListView(LoginRequiredMixin, View):
    template_name = 'category_expenses_list.html'

    def get(self, request, *args, **kwargs):
        form = CategoryExpensesForm()
        categories = CategoryExpenses.objects.filter(
            user=request.user)  # storing all existing expenses categories from database in this variable
        return render(request, self.template_name, {'categories': categories, 'form':form})

    def post(self, request):
        form = CategoryExpensesForm(request.POST)
        if form.is_valid():
            user = request.user
            categories = form.save(commit=False)
            categories.user = user
            categories.save()
            return redirect('category_expenses_list')
        return redirect(request, self.template_name, {'form': form})



class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)  # tworzenie instancji formularza
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            return redirect('contact_message', name=name, email=email)
        return render(request, 'contact.html', {'form': form})


class ContactMessageView(View):
    def get(self, request, name, email):
        return render(request, 'contact_message.html', {'name': name, 'email': email})


class MonthlyExpensesListView(LoginRequiredMixin, View):
    template_name = 'monthly_expenses_list.html'

    def get(self, request):
        expenses_wallet_form = ExpensesWalletForm()
        expenses_wallet_form.fields['category'].queryset = CategoryExpenses.objects.filter(user=request.user)
        expenses_wallet_form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)

        expenses = Expenses.objects.filter(user=request.user)
        form = FilterExpensesForm(request.GET)

        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        value_from = request.GET.get('value_from', '')
        value_to = request.GET.get('value_to', '')
        category_id = request.GET.get('category', '')

        if date_from == '':
            date_from = '1900-1-1'
        if date_to == '':
            date_to = '2900-1-1'
        if value_from == '':
            value_from = 0
        if value_to == '':
            value_to = 9999999999

        if category_id:
            expenses = expenses.filter(
                category=CategoryExpenses(id=category_id),
            )
        if value_to != '':
            expenses = expenses.filter(value__lte=value_to)

        if value_from != '':
            expenses = expenses.filter(value__gte=value_from)

        if date_from != '':
            expenses = expenses.filter(date__gte=date_from)

        if date_to != '':
            expenses = expenses.filter(date__lte=date_to)

        return render(request, self.template_name, {'expenses': expenses, 'expenses_wallet_form': expenses_wallet_form,
                                                    'expenses_search_form': form})

    def post(self, request):
        expenses_wallet_form = ExpensesWalletForm(request.POST)

        if expenses_wallet_form.is_valid():
            expense = expenses_wallet_form.save(commit=False)
            expense.user = request.user
            expense.save()
            wallet = expenses_wallet_form.cleaned_data['wallet']
            wallet.expenses.add(expense)
            return redirect('monthly_expenses_list')

        wallet = Wallet.objects.all().filter(user=request.user)
        expenses = Expenses.objects.all().filter(user=request.user)
        return render(request, self.template_name,
                      {'expenses_wallet_form': expenses_wallet_form, 'expenses': expenses, 'wallet': wallet})


class MonthlyIncomeListView(LoginRequiredMixin, View):
    template_name = 'monthly_income_list.html'

    def get(self, request, *args, **kwargs):
        income_wallet_form = IncomeWalletForm()
        income_wallet_form.fields['category'].queryset = CategoryIncome.objects.filter(user=request.user)
        income_wallet_form.fields['wallet'].queryset = Wallet.objects.filter(user=request.user)

        incomes = Income.objects.filter(user=request.user)
        form = FilterIncomeForm(request.GET)

        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        value_from = request.GET.get('value_from', '')
        value_to = request.GET.get('value_to', '')
        category_id = request.GET.get('category', '')

        if date_from == '':
            date_from = '1900-1-1'
        if date_to == '':
            date_to = '2900-1-1'
        if value_from == '':
            value_from = 0
        if value_to == '':
            value_to = 9999999999

        if category_id:
            incomes = incomes.filter(
                category=CategoryIncome(id=category_id),
            )
        if value_to != '':
            incomes = incomes.filter(value__lte=value_to)

        if value_from != '':
            incomes = incomes.filter(value__gte=value_from)

        if date_from != '':
            incomes = incomes.filter(date__gte=date_from)

        if date_to != '':
            incomes = incomes.filter(date__lte=date_to)

        return render(request, self.template_name,
                      {'incomes': incomes, 'income_wallet_form': income_wallet_form, 'income_search_form': form})

    def post(self, request, *args, **kwargs):
        income_wallet_form = IncomeWalletForm(request.POST)

        if income_wallet_form.is_valid():
            income = income_wallet_form.save(commit=False)
            income.user = request.user
            income.save()
            wallet = income_wallet_form.cleaned_data['wallet']
            wallet.incomes.add(income)
            return redirect('monthly_income_list')

        wallet = Wallet.objects.all().filter(user=request.user)
        incomes = Income.objects.all().filter(user=request.user)
        return render(request, self.template_name,
                      {'income_wallet_form': income_wallet_form, 'incomes': incomes, 'wallet': wallet})


class DetailedCategoryExpensesListView(View):
    template_name = 'detailed_category_expenses_list.html'

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(CategoryExpenses, pk=category_id, user=request.user)
        expenses = Expenses.objects.filter(category=category)
        return render(request, self.template_name, {'expenses': expenses, 'category': category})


class DetailedCategoryIncomeListView(View):
    template_name = 'detailed_category_income_list.html'

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(CategoryIncome, pk=category_id, user=request.user)
        incomes = Income.objects.filter(category=category)
        return render(request, self.template_name, {'incomes': incomes, 'category': category})



class ShowWalletsView(LoginRequiredMixin, View):
    template_name = 'wallets.html'

    def get(self, request):
        form = AddWalletForm()
        wallets = Wallet.objects.filter(user=request.user).all()
        return render(request, self.template_name, {'wallets': wallets, 'form': form})

    def post(self, request):
        form = AddWalletForm(request.POST)
        if form.is_valid():
            user = request.user
            wallet = form.save(commit=False)
            wallet.user = user
            wallet.save()
            return redirect('wallets')
        return render(request, self.template_name, {'form': form})


class EditWalletView(LoginRequiredMixin, UpdateView):
    model = Wallet
    fields = ['name']
    template_name = 'edit_form.html'
    success_url = reverse_lazy('wallets')


class DeleteWalletView(LoginRequiredMixin, DeleteView):
    model = Wallet
    template_name = 'delete_wallet.html'
    success_url = reverse_lazy('wallets')


class AddExpensesToWalletView(LoginRequiredMixin,View):
    template_name = 'add_income_expenses_to_wallet.html'

    def post(self, request, wallet_id, *args, **kwargs):
        expenses_form = ExpensesForm(request.POST)
        wallet = Wallet.objects.get(pk=wallet_id)

        if expenses_form.is_valid():
            expense = expenses_form.save(commit=False)
            expense.user = request.user
            expense.save()
            wallet.expenses.add(expense)
            return redirect('add_income_expense_to_wallet', wallet_id=wallet_id)

        wallet = Wallet.objects.all().filter(user=request.user)
        context = {
            'wallet': wallet,
            'expenses_form': expenses_form,
        }
        return render(request, self.template_name, context)


class AddIncomeToWalletView(View):
    template_name = 'add_income_expenses_to_wallet.html'

    def post(self, request, *args, wallet_id, **kwargs):
        income_form = IncomeForm(request.POST)
        wallet = Wallet.objects.get(pk=wallet_id)

        if income_form.is_valid():
            income = income_form.save(commit=False)
            income.user = request.user
            income.save()
            wallet.incomes.add(income)
            return redirect('add_income_expense_to_wallet', wallet_id=wallet_id)
        wallet = Wallet.objects.all().filter(user=request.user)
        context = {
            'wallet': wallet,
            'income_form': income_form,
        }
        return render(request, self.template_name, context)

class AddIncomeExpensesToWalletView(View):
    template_name = 'add_income_expenses_to_wallet.html'

    def get(self, request, *args, wallet_id, **kwargs):
        income_form = IncomeForm()
        expenses_form = ExpensesForm()
        income_form.fields['category'].queryset = CategoryIncome.objects.filter(user=request.user)
        expenses_form.fields['category'].queryset = CategoryExpenses.objects.filter(user=request.user)

        wallet = Wallet.objects.get(pk=wallet_id)
        incomes = wallet.incomes.all()
        expenses = wallet.expenses.all()

        context = {
            'wallet': wallet,
            'incomes': incomes,
            'expenses': expenses,
            'income_form': income_form,
            'expenses_form': expenses_form
        }
        return render(request, self.template_name, context)

class EditAddIncomeToWalletView(LoginRequiredMixin, UpdateView):
    model = Income
    fields = ['value']
    template_name = 'edit_form.html'
    success_url = reverse_lazy('wallets')


class DeleteAddIncomeToWalletView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = 'delete_income.html'
    success_url = reverse_lazy('wallets')


class EditAddExpensesToWalletView(LoginRequiredMixin, UpdateView):
    model = Expenses
    fields = ['value']
    template_name = 'edit_form.html'
    success_url = reverse_lazy('wallets')


class DeleteAddExpensesToWalletView(LoginRequiredMixin, DeleteView):
    model = Expenses

    template_name = 'delete_expense.html'
    success_url = reverse_lazy('wallets')

class EditMonthlyIncomeListView(LoginRequiredMixin, UpdateView):
    model = Income
    fields = ['value']
    template_name = 'edit_form.html'
    success_url = reverse_lazy('monthly_income_list')


class DeleteMonthlyIncomeListView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = 'delete_income.html'
    success_url = reverse_lazy('monthly_income_list')


class EditMonthlyExpensesListView(LoginRequiredMixin, UpdateView):
    model = Expenses
    fields = ['value']
    template_name = 'edit_form.html'
    success_url = reverse_lazy('monthly_expenses_list')


class DeleteMonthlyExpensesListView(LoginRequiredMixin, DeleteView):
    model = Expenses
    template_name = 'delete_expense.html'
    success_url = reverse_lazy('monthly_expenses_list')

