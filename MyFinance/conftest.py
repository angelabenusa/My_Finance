

from MyFinance.models import *
import pytest
@pytest.fixture
def home_page():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryIncome.objects.create(name="Salary", user=user)
    income = Income.objects.create(user=user, value=100, date='2023-12-20', category=category)
    income1 = Income.objects.create(user=user, value=200, date='2021-12-20', category=category)
    return category, income, income1, user

@pytest.fixture
def home_page1():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryIncome.objects.create(name='Salary', user=user)
    income = Income.objects.create(user=user, category=category, value=100, date='2023-12-23')
    return category, user, income

@pytest.fixture
def add_category_income_view_get():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def add_category_income_view_post():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def category_income_list_view_get():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def logout_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def category_income_list_view_post():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryIncome.objects.create(name='Salary', user=user)
    return category, user

@pytest.fixture
def edit_category_income_list_view():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryIncome.objects.create(user=user, name='testcategory')
    return category, user

@pytest.fixture
def edit_category_income_list_view_negative():
    user = User.objects.create_user(username='test user', password='testpassword')
    return user

@pytest.fixture
def category_income_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def edit_category_expenses_list_view():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryExpenses.objects.create(user=user,name='testcategory')
    return category, user

@pytest.fixture
def edit_category_expenses_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def delete_category_income_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def delete_category_income_list_view():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryIncome.objects.create(user=user, name='testcategory')
    return category, user

@pytest.fixture
def delete_category_expenses_list_view():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryExpenses.objects.create(user=user, name='testcategory')
    return category, user

@pytest.fixture
def delete_category_expenses_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def add_category_expenses_view_get():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def add_category_expenses_view_post():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def category_expenses_list_view_get():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def category_expenses_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def category_expenses_list_view_post():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryExpenses.objects.create(user=user, name='testcategory')
    return category, user

@pytest.fixture
def category_expenses_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def monthly_expenses_list_view_get():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryExpenses.objects.create(user=user, name='testcategory')
    wallet = Wallet.objects.create(name='Main Wallet', user=user)
    expenses = Expenses.objects.create(
        user=user,
        category=category,
        wallet=wallet,
        date='2022-02-15',
        value=100
    )
    return category,  wallet, expenses, user

@pytest.fixture
def monthly_expenses_list_view_post():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryExpenses.objects.create(name='Food', user=user)
    wallet = Wallet.objects.create(name='Main Wallet', user=user)
    expense = Expenses.objects.create(user=user, value=100, date='2023-12-23', category=category, wallet=wallet)
    return category, expense, wallet, user

@pytest.fixture
def monthly_income_list_view_get():
    user = User.objects.create_user(username='test user', password='testpassword')
    category = CategoryIncome.objects.create(name='Contract', user=user)
    wallet = Wallet.objects.create(name='Main Wallet', user=user)
    income = Income.objects.create(category=category, wallet=wallet, user=user, date='2023-12-23', value=5000)
    return category, wallet, income, user



@pytest.fixture
def monthly_income_list_view_post():
    user = User.objects.create_user(username='test user', password='1234')
    category = CategoryIncome.objects.create(name='Contract', user=user)
    wallet = Wallet.objects.create(name='Main Wallet', user=user)
    # incomes = Income.objects.create(category=category, value=5000, user=user, date='2023-12-23')
    return category, wallet, user #incomes

@pytest.fixture
def detailed_category_expenses_list_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryExpenses.objects.create(name='TestCategory', user=user)
    expense = Expenses.objects.create(category=category, value=50, user=user, date='2023-12-23')
    return category, user, expense


@pytest.fixture
def detailed_category_expenses_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def detailed_category_income_list_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryIncome.objects.create(name='TestCategory', user=user)
    incomes = Income.objects.create(user=user, category=category, value=50, date='2023-12-23')
    return category, user, incomes


@pytest.fixture
def detailed_category_income_list_view_negative():
    user = User.objects.create_user(username='unique_user123', password='a123')
    category = CategoryIncome.objects.create(name='TestCategory', user=user)
    return category, user


@pytest.fixture
def show_wallets_view_get():
    user = User.objects.create_user(username='qwer123', password='qwer123')
    wallet = Wallet.objects.create(user=user, name='test wallet')
    return wallet, user


@pytest.fixture
def show_wallets_view_post():
    user = User.objects.create_user(username='uytr1234', password='uytr1234')
    wallet = Wallet.objects.create(user=user, name='test wallet')
    return wallet, user


@pytest.fixture
def edit_wallet_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(name='test wallet', user=user)
    return wallet, user


@pytest.fixture
def edit_wallet_view_negative():
    user = User.objects.create_user(username='awq`12', password='testpassword')
    wallet = Wallet.objects.create(name='test wallet', user=user)
    return wallet, user


@pytest.fixture
def delete_wallet_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(name='test wallet', user=user)
    return wallet, user

@pytest.fixture
def delete_wallet_view_negative():
    user = User.objects.create_user(username='765gf', password='testpassword')
    wallet = Wallet.objects.create(name='test wallet', user=user)
    return wallet, user


@pytest.fixture
def add_expenses_to_wallet_view_post():
    user = User.objects.create_user(username='iiu9867', password='testpassword')
    wallet = Wallet.objects.create(user=user, name='Test Wallet')
    return wallet, user
@pytest.fixture
def add_expenses_to_wallet_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(user=user, name='Test Wallet')
    return wallet, user

@pytest.fixture
def add_income_to_wallet_view_post():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(user=user, name='Test Wallet')
    return wallet, user

@pytest.fixture
def add_income_to_wallet_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(user=user, name='Test Wallet')
    return wallet, user

@pytest.fixture
def add_income_expenses_to_wallet_view_get():
    user = User.objects.create_user(username='afr123', password='testpassword')
    wallet = Wallet.objects.create(name='test wallet', user=user)
    category_income = CategoryIncome.objects.create(name='Salary', user=user)
    category_expenses = CategoryExpenses.objects.create(name='Groceries', user=user)
    return wallet, category_income, category_expenses, user

@pytest.fixture
def add_income_expenses_to_wallet_view_get_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(name='test wallet', user=user)
    category_income = CategoryIncome.objects.create(name='Salary', user=user)
    category_expenses = CategoryExpenses.objects.create(name='Groceries', user=user)
    return wallet, category_income, category_expenses, user

@pytest.fixture
def edit_add_income_to_wallet_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(name='Test Wallet', user=user)
    category = CategoryIncome.objects.create(name='Salary', user=user)
    income = Income.objects.create(value=500, date='2023-12-23', category=category, user=user)
    return wallet, category, income, user

@pytest.fixture
def edit_add_income_to_wallet_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(name='Test Wallet', user=user)
    return wallet, user

@pytest.fixture
def edit_add_expenses_to_wallet_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(name='Test Wallet', user=user)
    category = CategoryExpenses.objects.create(name='Kindergarten', user=user)
    expense = Expenses.objects.create(value=100, date='2023-12-23', category=category, user=user)
    return wallet, expense, category, user

@pytest.fixture
def edit_add_expenses_to_wallet_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    wallet = Wallet.objects.create(name='Test Wallet', user=user)
    category = CategoryExpenses.objects.create(name='Kindergarten', user=user)
    expenses = Expenses.objects.create(value=100, date='2023-12-23', category=category, user=user)
    return wallet, expenses, category, user


@pytest.fixture
def edit_monthly_income_list_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryIncome.objects.create(name='B2B', user=user)
    income = Income.objects.create(value=1000, category=category, date='2023-12-23', user=user)
    return category, income, user

@pytest.fixture
def edit_monthly_income_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryIncome.objects.create(name='B2B', user=user)
    income = Income.objects.create(value=1000, category=category, date='2023-12-23', user=user)
    return category, income, user

@pytest.fixture
def delete_monthly_income_list_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryIncome.objects.create(name='B2B', user=user)
    income = Income.objects.create(value=1000, category=category, date='2023-12-23', user=user)
    return income, category, user


@pytest.fixture
def delete_monthly_income_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryIncome.objects.create(name='B2B', user=user)
    income = Income.objects.create(value=1000, category=category, date='2023-12-23', user=user)
    return category, income, user


@pytest.fixture
def edit_monthly_expenses_list_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryExpenses.objects.create(name='Shopping', user=user)
    expense = Expenses.objects.create(value=500, category=category, date='2023-12-23', user=user)
    return category, expense, user


@pytest.fixture
def edit_monthly_expenses_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryExpenses.objects.create(name='Shopping', user=user)
    expense = Expenses.objects.create(value=500, category=category, date='2023-12-23', user=user)
    return category, expense, user


@pytest.fixture
def delete_monthly_expenses_list_view_positive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryExpenses.objects.create(name='Shopping', user=user)
    expense = Expenses.objects.create(value=500, category=category, date='2023-12-23', user=user)
    return category, expense, user


@pytest.fixture
def delete_monthly_expenses_list_view_negative():
    user = User.objects.create_user(username='testuser', password='testpassword')
    category = CategoryExpenses.objects.create(name='Shopping', user=user)
    expense = Expenses.objects.create(value=500, category=category, date='2023-12-23', user=user)
    return category, expense, user



