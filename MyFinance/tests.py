from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template.response import TemplateResponse

from django.test import TestCase
import pytest
from django.urls import reverse
from django.test import Client
from django.utils import timezone

from MyFinance.forms import CategoryIncomeForm, CategoryExpensesForm
from MyFinance.models import Income, CategoryIncome, CategoryExpenses, Expenses, Wallet


# Create your tests here.

# positive
@pytest.mark.django_db  # test will be using database, permitting to use it
def test_login_view_positive():
    client = Client()
    username = 'testuser'
    password = 'testpassword'
    User.objects.create_user(username=username, password=password)
    login_data = {'username': username, 'password': password}
    response = client.post('/login/', login_data)

    assert response.status_code == 302  # expected status code
    assert response.wsgi_request.user.is_authenticated  # checking if user logged in


# positive
@pytest.mark.django_db
def test_login_view_negative():
    client = Client()
    invalid_login_data = {'username': 'invalliduser', 'password': 'invalidpassword'}
    response = client.post('/login/', invalid_login_data, follow=True)

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated  # checking if user in not logged in
    assert 'form_generic.html' in [template.name for template in
                                   response.templates]  # checking if logging form is showing


# positive
@pytest.mark.django_db
def test_logout_view_positive(logout_view_positive):
    client = Client()
    user = logout_view_positive
    client.login(username='testuser', password='testpassword')

    response = client.get('/logout/')

    assert response.status_code == 302  # expented status - redirecting
    assert response.url == '/wallets/'
    assert not response.wsgi_request.user.is_authenticated


# positive
@pytest.mark.django_db
def test_logout_view_negative():
    client = Client()
    response = client.get('/logout/')

    assert response.status_code == 302
    assert response.url == '/wallets/'
    assert response.wsgi_request.user.is_anonymous  # after logout user is anonymous


# positive
@pytest.mark.django_db
def test_user_create_view_get():
    client = Client()
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


# positive
@pytest.mark.django_db
def test_user_create_view_post():
    client = Client()
    url = reverse('register')
    data = {
        'username': 'testusername',
        'password': 'testpassword',
        'password2': 'testpassword'
    }
    response = client.post(url, data)
    assert response.status_code == 302


# positive
@pytest.mark.django_db
def test_home_page_account_balanse_view_get(home_page):
    client = Client()
    client.login(username='test user', password='testpassword')  # loggining user
    valid_date = date(2023, 11, 21)
    category, income, income1, user = home_page

    url = reverse('homepage_with_account_balance')
    response = client.get(url)
    assert response.status_code == 200


#     response.context["tygrysek"]


# positive
@pytest.mark.django_db
def test_home_page_account_balanse_view_1(home_page1):
    client = Client()
    client.login(username='testuser', password='testpassword')
    income, _, _ = home_page1

    url = reverse('homepage_with_account_balance')
    response = client.get(url)

    assert response.status_code == 302  # Check for a successful response code
    # assert 'homepage_with_account_balance' in response.templates[0].name
    # assert response.url == '/login/?next=/'

    # assert 'total_income' in response.context  # checking provided context
    # assert response.context['total_income'] == 100


# positive
@pytest.mark.django_db
def test_add_category_income_view_get(add_category_income_view_get):
    client = Client()
    user = add_category_income_view_get
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('add_category_income')
    response = client.get(url)
    assert response.status_code == 200


# positive
@pytest.mark.django_db
def test_add_category_income_view_post(add_category_income_view_post):
    client = Client()
    user = add_category_income_view_post
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('add_category_income')
    data = {
        'name': 'testcategory'
    }
    response = client.post(url, data)
    assert response.status_code == 302


# positive
@pytest.mark.django_db
def test_category_income_list_view_get(category_income_list_view_get):
    client = Client()
    user = category_income_list_view_get
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('category_income_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'category_income_list' in response.templates[0].name
    assert isinstance(response.context['form'], CategoryIncomeForm)


# positive
@pytest.mark.django_db
def test_category_income_list_view_post(category_income_list_view_post):
    client = Client()
    user, category = category_income_list_view_post
    client.login(username='testuser', password='testpassword')  # loggining user

    data = {'name': 'Test Category'}

    url = reverse('category_income_list')
    response = client.get(url, data=data)

    assert response.status_code == 302

    assert response.url == reverse('category_income_list')
    assert CategoryIncome.objects.filter(user=user, name='Test Category').exists()


# positive
@pytest.mark.django_db
def test_category_income_list_view_negative(category_income_list_view_negative):
    CategoryIncome.objects.all().delete()

    client = Client()
    user = category_income_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('category_income_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'category_income_list' in response.templates[0].name
    assert 'categories' in response.context
    assert len(response.context['categories']) == 0  # checking if there is no categories


# positive
@pytest.mark.django_db
def test_edit_category_income_list_view(edit_category_income_list_view):
    client = Client()
    user, category = edit_category_income_list_view
    client.login(username='testuser', password='testpassword')  # loggining user

    category = edit_category_income_list_view
    url = reverse('edit_category_income_list', kwargs={'pk': category.pk})

    updated_name = 'updated_testcategory'
    data = {'name': updated_name}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('category_income_list')

    updated_category = CategoryIncome.objects.get(pk=category.pk)
    assert updated_category.name == updated_name


# positive
@pytest.mark.django_db
def test_edit_category_income_list_view_negative(edit_category_income_list_view_negative):
    client = Client()
    user = edit_category_income_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('edit_category_income_list',
                  kwargs={'pk': 1})
    response = client.get(url)

    assert response.status_code == 302


# positive
@pytest.mark.django_db
def test_edit_category_expenses_list_view(edit_category_expenses_list_view):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    category, user = edit_category_expenses_list_view
    url = reverse('edit_category_expenses_list', kwargs={'pk': category.pk})

    updated_name = 'testcategory'
    data = {'name': updated_name}
    response = client.post(url, data)
    assert response.status_code == 302

    updated_category = CategoryExpenses.objects.get(pk=category.pk)
    assert updated_category.name == updated_name


# positive
@pytest.mark.django_db
def test_edit_category_expenses_list_view_negative(edit_category_expenses_list_view_negative):
    client = Client()
    user = edit_category_expenses_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('edit_category_expenses_list',
                  kwargs={'pk': 1})
    response = client.get(url)

    assert response.status_code == 404


# positive
@pytest.mark.django_db
def test_delete_category_income_list_view(delete_category_income_list_view):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    category, user = delete_category_income_list_view
    url = reverse('delete_category_income_list', kwargs={'pk': category.pk})

    response = client.get(url)
    assert response.status_code == 302
    assert 'delete_form' in response.templates[0].name

    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('category_income_list')
    assert not CategoryIncome.objects.filter(user=user, pk=category.pk).exists()


# positive
@pytest.mark.django_db
def test_delete_category_income_list_view_negative(delete_category_income_list_view_negative):
    client = Client()
    user = delete_category_income_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('delete_category_income_list', kwargs={'pk': 1})
    response = client.get(url)

    assert response.status_code == 404  # expect a 403 status code because the deletion attempt requires a POST method and this is a GET call


# positive
@pytest.mark.django_db
def test_delete_category_expenses_list_view(delete_category_expenses_list_view):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    category, user = delete_category_expenses_list_view
    delete_url = reverse('delete_category_expenses_list', kwargs={'pk': category.pk})

    response = client.get(delete_url)
    assert response.status_code == 302
    assert 'delete_form' in response.templates[0].name

    response = client.post(delete_url)
    assert response.status_code == 302
    assert not CategoryExpenses.objects.filter(user=user, pk=category.pk).exists()


# positive
@pytest.mark.django_db
def test_delete_category_expenses_list_view_negative(delete_category_expenses_list_view_negative):
    client = Client()
    user = delete_category_expenses_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('delete_category_expenses_list', kwargs={'pk': 1})
    response = client.get(url)

    assert response.status_code == 404


# negative
@pytest.mark.django_db
def test_category_expenses_list_view_negative(category_expenses_list_view_negative):
    client = Client()
    user = category_expenses_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('category_expenses_list')
    response = client.get(url)

    assert response.status_code == 404  # expect a 405 status code because the view only uses the 'get' method and does not support other methods


# positive
@pytest.mark.django_db
def test_add_category_expenses_view_get(add_category_expenses_view_get):
    client = Client()
    user = add_category_expenses_view_get
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('add_category_expenses')
    response = client.post(url)
    assert response.status_code == 200


# positive
@pytest.mark.django_db
def test_add_category_expenses_view_post(add_category_expenses_view_post):
    client = Client()
    user = add_category_expenses_view_post
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('add_category_expenses')
    data = {
        'name': 'testcategory'
    }
    response = client.post(url, data)
    assert response.status_code == 302


# positive
@pytest.mark.django_db
def test_category_expenses_list_view_get(category_expenses_list_view_get):
    client = Client()
    user = category_expenses_list_view_get
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('category_expenses_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'category_expenses_list.html' in response.templates[0].name

    assert 'form' in response.context
    assert 'categories' in response.context

    assert isinstance(response.context['form'], CategoryExpensesForm)


# positive
@pytest.mark.django_db
def test_category_expenses_list_view_post(category_expenses_list_view_post):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user
    user, category = category_expenses_list_view_post

    data = {'name': 'Test Expense Category'}
    url = reverse('category_expenses_list')
    response = client.post(url, data=data)

    assert response.status_code == 302
    assert response.url == reverse('/login/?next=/category_expenses_list/')
    assert CategoryExpenses.objects.filter(user=user, name='Test Expense Category').exists()


# positive
@pytest.mark.django_db
def test_category_expenses_list_view_negative(category_expenses_list_view_negative):
    client = Client()
    user = category_expenses_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('category_expenses_list')
    response = client.get(url)

    assert response.status_code == 200
    assert not CategoryExpenses.objects.filter(user=user, name='Test Expense Category').exists()


# negative
@pytest.mark.django_db
def test_about_view_positive():
    client = Client()
    url = reverse('about')
    response = client.get(url)

    assert response.status_code == 200
    assert response.url == reverse('about')

    # assert 'about.html' in response.templates[0].name


# negative
@pytest.mark.django_db
def test_about_view_negative():
    client = Client()
    url = reverse('about')
    response = client.get(url)

    assert response.status_code == 404
    assert 'about' in response.templates[0].name


# positive
@pytest.mark.django_db
def test_contact_view_get():
    client = Client()
    url = reverse('contact')
    response = client.get(url)

    assert response.status_code == 200
    assert 'contact' in response.templates[0].name


# positive
@pytest.mark.django_db
def test_contact_view_post():
    client = Client()
    url = reverse('contact')
    data = {
        'name': 'testname',
        'email': 'testemail@hotmail.com'
    }
    response = client.post(url, data)
    assert response.status_code == 200


# positive
@pytest.mark.django_db
def test_contact_message_view_positive():
    client = Client()
    name = 'testname'
    email = 'testemail@hotmail.com'
    url = reverse('contact_message', args=(name, email))
    response = client.get(url)

    assert response.status_code == 200
    assert 'contact_message' in response.templates[0].name
    assert response.context['name'] == name
    assert response.context['email'] == email


# positive
@pytest.mark.django_db
def test_contact_message_view_negative():
    client = Client()
    name = 'testname'
    email = 'testemail@hotmail.com'
    invalid_name = 'invalid_name'
    invalid_email = 'invalid_email@hotmail.com'

    url = reverse('contact_message', args=(name, email))
    response = client.get(url)

    assert response.status_code == 200
    assert 'contact_message' in response.templates[0].name
    assert response.context['name'] == name
    assert response.context['email'] == email

    invalid_url = reverse('contact_message', args=(invalid_name, invalid_email))

    try:
        response = client.get(invalid_url)
        assert response.status_code == 200
    except Http404:
        pass


# positive
@pytest.mark.django_db
def test_monthly_expenses_list_view_get(monthly_expenses_list_view_get):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user
    category, wallet, expenses, user = monthly_expenses_list_view_get

    url = reverse('monthly_expenses_list')
    response = client.get(url)

    assert response.status_code == 302
    # assert 'monthly_expenses_list' in response.templates[0].name

    # expenses = response.context['expenses']
    # assert len(expenses) == 1
    # assert expenses[0] in Expenses.objects.all()
    # assert expenses[0].value == 100


# positive
@pytest.mark.django_db
def test_monthly_expenses_list_view_post(monthly_expenses_list_view_post):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    category, _, wallet, user = monthly_expenses_list_view_post
    #
    form_data = {
        'date': '2022-02-15',
        'value': 100,
        'category': category.id,
        'wallet': wallet.id,
        # 'expense': expense
    }
    url = reverse('monthly_expenses_list')
    # response = client.get(url)
    response = client.post(url, form_data)
    assert response.status_code == 302
    # try:
    #     expense = Expenses.objects.get(user=user, category=category.id)
    # except Expenses.DoesNotExist:
    #     expense = None
    expenses = Expenses.objects.filter(user=user, category=category.id)
    assert expenses.count() == 2, "Expected exactly two expenses"
    expense = expenses.first()

    # expense = Expenses.objects.get(user=user, category=category.id)

    assert expense is not None
    assert expense.value == 100
    assert expense.user == user


# positive
@pytest.mark.django_db
def test_monthly_income_list_view_get(monthly_income_list_view_get):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user
    category, wallet, income, user = monthly_income_list_view_get

    url = reverse('monthly_income_list')
    response = client.get(url)

    assert response.status_code == 302
    # assert 'monthly_income_list' in response.templates[0].name

    # incomes = response.context['incomes']
    # assert len(incomes) == 1
    # assert incomes[0] in Income.objects.all()
    assert 'login' in response.url


# positive
@pytest.mark.django_db
def test_monthly_income_list_view_post(monthly_income_list_view_post):
    client = Client()
    client.login(username='test_user_post', password='1234')  # loggining user

    category, wallet, user = monthly_income_list_view_post

    form_data = {
        'date': '2022-02-15',
        'value': 1000,
        'category': category.id,
        'wallet': wallet.id
    }
    url = reverse('monthly_income_list')
    response = client.post(url, form_data)
    assert response.status_code == 302
    try:
        incomes = Income.objects.get(user=user, category=category.id)
    except ObjectDoesNotExist:
        incomes = None
    # assert incomes.value == 1000
    # assert incomes.user == user


# positive
@pytest.mark.django_db
def test_detailed_category_expenses_list_view(detailed_category_expenses_list_view):
    client = Client()
    client.login(username='angela', password='angela123')  # loggining user

    user, category, expense = detailed_category_expenses_list_view

    # url = reverse('detailed_category_expenses_list')
    url = reverse('detailed_category_expenses_list', kwargs={'category_id': category.id})
    response = client.get(url)

    assert response.status_code == 200

    assert 'category' in response.context
    assert response.context['category'] == category

    assert 'detailed_category_expenses_list.html' in response.templates[0].name


# positive
@pytest.mark.django_db
def test_detailed_category_expenses_list_view_negative(detailed_category_expenses_list_view_negative):
    client = Client()
    user = detailed_category_expenses_list_view_negative
    client.login(username='testuser', password='testpassword')  # loggining user

    url = reverse('detailed_category_expenses_list', kwargs={'category_id': 1})
    response = client.get(url)
    assert response.status_code == 404
    # assert response.url == reverse('detailed_category_expenses_list')


# positive
@pytest.mark.django_db
def test_detailed_category_income_list_view(detailed_category_income_list_view):
    client = Client()
    # user = User.objects.create_user(username='ang123', password='ang123')
    client.login(username='ang123', password='ang123')  # loggining user
    #
    # category = CategoryIncome.objects.create(name='TestCategory', user=user)
    # incomes = Income.objects.create(user=user, category=category, value=50, date='2023-12-23')
    user, category, incomes = detailed_category_income_list_view

    url = reverse('detailed_category_income_list', kwargs={'category_id': category.id})
    response = client.get(url)

    assert response.status_code == 200

    assert 'category' in response.context
    assert response.context['category'] == category
    assert response.context['incomes'].first() == incomes

    # assert 'detailed_category_income_list.html' in response.template_name[0].name
    assert 'detailed_category_income_list.html' in [template.name for template in response.templates]


# negative UNIQUE
@pytest.mark.django_db
def test_detailed_category_income_list_view_negative(detailed_category_income_list_view_negative):
    client = Client()
    # user = User.objects.create_user(username='unique_user123', password='a123')
    # client.login(username='testuser', password='testpassword')  # loggining user
    # category = CategoryIncome.objects.create(name='TestCategory', user=user)
    category, user = detailed_category_income_list_view_negative
    url = reverse('detailed_category_income_list', kwargs={'category_id': category.id})
    response = client.get(url)
    assert response.status_code == 404
    assert response.url == reverse('login')


# negative UNIQUE
@pytest.mark.django_db
def test_show_wallets_view_get(show_wallets_view_get):
    client = Client()
    client.login(username='qwer123', password='qwer123')  # loggining user

    wallet, user = show_wallets_view_get
    url = reverse('wallets')
    response = client.get(url)
    assert response.status_code == 200

    assert 'wallets' in response.context
    assert list(response.context['wallets']) == [wallet]
    assert 'wallets' in response.templates[0].name
    assert b'test wallet' in response.content


# negative UNIQUE
@pytest.mark.django_db
def test_show_wallets_view_post(show_wallets_view_post):
    client = Client()
    client.login(username='uytr1234', password='uytr1234')  # loggining user

    wallet, user = show_wallets_view_post
    form_data = {
        'name': 'new wallet'
    }
    url = reverse('wallets')
    # response = client.post(url)
    response = client.post(url, data=form_data)

    assert response.status_code == 200
    assert 'wallets' in response.url()
    assert Wallet.objects.filter(user=user, name='new wallet').exists()


# negative UNIQUE
@pytest.mark.django_db
def test_edit_wallet_view_positive(edit_wallet_view_positive):
    client = Client()
    # user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')  # loggining user

    # wallet = Wallet.objects.create(name='test wallet', user=user)
    wallet, user = edit_wallet_view_positive
    form_data = {
        'name': 'test wallet'
    }
    url = reverse('edit_wallet', kwargs={'pk': wallet.id})
    response = client.get(url, data=form_data)

    assert response.status_code == 200
    assert response.url == reverse('edit_wallet')

    wallet.refresh_from_db()
    assert wallet.name == 'test wallet'


# negative
@pytest.mark.django_db
def test_edit_wallet_view_negative(edit_wallet_view_negative):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    wallet, user = edit_wallet_view_negative
    form_data = {
        'name': ''
    }
    # url = reverse('edit_wallet')
    url = reverse('edit_wallet', kwargs={'pk': wallet.id})
    response = client.get(url, data=form_data)
    # response = client.get(url)

    assert response.status_code == 302
    assert 'edit_form' in response.templates[0].name

    # wallet.refresh_from_db()
    # user.refresh_from_db()
    # assert wallet.name == 'test wallet'


# positive
@pytest.mark.django_db
def test_delete_wallet_view_positive(delete_wallet_view_positive):
    client = Client()
    client.login(username='awq12', password='testpassword')  # loggining user

    wallet, user = delete_wallet_view_positive
    url = reverse('delete_wallet', kwargs={'pk': wallet.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert Wallet.objects.filter(pk=wallet.pk).exists()

    # wallet.refresh_from_db()
    # assert wallet.name == 'test wallet'


# negative UNIQUE
@pytest.mark.django_db
def test_delete_wallet_view_negative(delete_wallet_view_negative):
    client = Client()
    client.login(username='765gf', password='testpassword')  # loggining user

    wallet, user = delete_wallet_view_negative
    url = reverse('delete_wallet')
    response = client.get(url, kwargs={'pk': wallet.pk})

    assert response.status_code == 302
    assert not Wallet.objects.filter(pk=wallet.pk).exists()


# negative UNIQUE
@pytest.mark.django_db
def test_add_expenses_to_wallet_view_post(add_expenses_to_wallet_view_post):
    client = Client()
    client.login(username='iiu9867', password='testpassword')  # loggining user

    wallet, user = add_expenses_to_wallet_view_post
    data = {
        'value': 50,
        'category': 'Shopping',
        'date': '12-12-2023'
    }
    url = reverse('add_income_expenses_to_wallet')
    # response = client.post(url)
    response = client.post(url, kwargs={'wallet_id': wallet.id, 'data': data})

    assert response.status_code == 302
    assert Expenses.objects.filter(category='Shopping', value=50).exists()
    # expenses.refresh_from_db()
    # assert expenses.value == 50


# negative UNIQUE
@pytest.mark.django_db
def test_add_expenses_to_wallet_view_negative(add_expenses_to_wallet_view_negative):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    # wallet = Wallet.objects.create(user=user, name='Test Wallet')
    wallet, user = add_expenses_to_wallet_view_negative
    data = {
        'value': -100,
        'category': 'Shopping',
        'date': '12-12-2023'
    }
    url = reverse('add_income_expenses_to_wallet')
    response = client.post(url, kwargs={'wallet_id': wallet.id, 'data': data})

    assert response.status_code == 302
    assert not Expenses.objects.filter(category='Shopping', value=50).exists()


# negative UNIQUE
@pytest.mark.django_db
def test_add_income_to_wallet_view_post(add_income_to_wallet_view_post):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user
    wallet, user = add_income_to_wallet_view_post
    data = {
        'value': 5000,
        'category': 'Contract',
        'date': '12-12-2023'
    }
    url = reverse('add_income_expenses_to_wallet')
    response = client.post(url, kwargs={'wallet_id': wallet.id, 'data': data})

    assert response.status_code == 302
    assert Income.objects.filter(category='Contract', value=5000).exists()
    # income.refresh_from_db()
    # assert income.value == 50


# negative fixture 'add_income_to_wallet_view_negative' not found
@pytest.mark.django_db
def test_add_income_to_wallet_view_negative(add_income_to_wallet_view_negative):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    wallet, user = add_income_to_wallet_view_negative
    data = {
        'value': -100,
        'category': 'Contract',
        'date': '12-12-2023'
    }
    url = reverse('add_income_expenses_to_wallet')
    response = client.post(url, kwargs={'wallet_id': wallet.id, 'data': data})

    assert response.status_code == 302
    assert Income.objects.filter(category='Contract', value=50).exists()


# negative UNIQUE
@pytest.mark.django_db
def test_add_income_expenses_to_wallet_view_get(add_income_expenses_to_wallet_view_get):
    client = Client()
    client.login(username='afr123', password='testpassword')  # logging in the user

    wallet, income_form_data, expense_form_data, user = add_income_expenses_to_wallet_view_get

    url = reverse('add_income_expenses_to_wallet', kwargs={'wallet_id': wallet.id})
    response = client.get(url, income_form_data, expense_form_data)

    assert response.status_code == 200
    assert 'add_income_expenses_to_wallet' in response.templates[0].name


# negative UNIQUE
@pytest.mark.django_db
def test_add_income_expenses_to_wallet_view_get_negative(add_income_expenses_to_wallet_view_get_negative):
    client = Client()
    client.login(username='testuser', password='testpassword')  # loggining user

    wallet, category_income, category_expenses, user = add_income_expenses_to_wallet_view_get_negative

    income_form_data = {
        'category': category_income.id,
        'value': -987,
    }

    expense_form_data = {
        'category': category_expenses.id,
        'value': -344,
    }
    url = reverse('add_income_expenses_to_wallet', kwargs={'wallet_id': wallet.id})
    response = client.get(url, income_form_data, expense_form_data)

    assert response.status_code == 200
    assert 'add_income_expenses_to_wallet' in response.templates[0].name


# negative UNIQUE
@pytest.mark.django_db
def test_edit_add_income_to_wallet_view_positive(edit_add_income_to_wallet_view_positive):
    client = Client()
    client.login(username='testuser', password='testpassword')

    # wallet = Wallet.objects.create(name='Test Wallet', user=user)
    # category = CategoryIncome.objects.create(name='Salary', user=user)
    # income = Income.objects.create(value=500, date='2023-12-23', category=category, user=user)
    wallet, category, income, user = edit_add_income_to_wallet_view_positive
    wallet.incomes.add(income)

    form_data = {
        'value': 500.00,
    }
    url = reverse('edit_add_income_to_wallet', kwargs={'pk': income.pk})
    response = client.post(url, data=form_data)

    assert response.status_code == 302

    income.refresh_from_db()
    assert income.value == 700.00


# negative UNIQUE
@pytest.mark.django_db
def test_edit_add_income_to_wallet_view_negative(edit_add_income_to_wallet_view_negative):
    client = Client()
    client.login(username='testuser', password='testpassword')
    wallet, user = edit_add_income_to_wallet_view_negative

    form_data = {
        'date': '2022-02-22',
    }
    url = reverse('edit_add_income_to_wallet', args=[wallet.id])
    response = client.post(url, data=form_data)
    assert response.status_code == 404


# negative UNIQUE
@pytest.mark.django_db
def test_edit_add_expenses_to_wallet_view_negative(edit_add_expenses_to_wallet_view_negative):

    client = Client()
    client.login(username='testuser', password='testpassword')

    wallet, expense, category, user = edit_add_expenses_to_wallet_view_negative
    wallet.expenses.add(expense)

    form_data = {
        'value': 100,
    }

    url = reverse('edit_add_expenses_to_wallet', kwargs={'pk': expense.pk})
    response = client.post(url, data=form_data)

    assert response.status_code == 302

    expense.refresh_from_db()
    assert expense.value == -500


# negative UNIQUE
@pytest.mark.django_db
def test_edit_add_expenses_to_wallet_view_positive(edit_add_expenses_to_wallet_view_positive):

    client = Client()
    client.login(username='testuser', password='testpassword')

    wallet, expenses, category, user = edit_add_expenses_to_wallet_view_positive
    wallet.expenses.add(expenses)

    form_data = {
        'value': 300,
    }

    url = reverse('edit_add_expenses_to_wallet', kwargs={'pk': expenses.pk})
    response = client.post(url, data=form_data)

    assert response.status_code == 302

    expenses.refresh_from_db()
    assert expenses.value == 300


# negative UNIQUE
@pytest.mark.django_db
def test_edit_monthly_income_list_view_positive(edit_monthly_income_list_view_positive):

    client = Client()
    client.login(username='testuser', password='testpassword')

    category, income, user = edit_monthly_income_list_view_positive

    form_data = {
        'value': 1200,
    }

    url = reverse('edit_monthly_income_list', kwargs={'pk': income.pk})
    response = client.post(url, data=form_data)

    assert response.status_code == 302

    income.refresh_from_db()
    assert income.value == 1200


# negative UNIQUE
@pytest.mark.django_db
def test_edit_monthly_income_list_view_negative(edit_monthly_income_list_view_negative):
    client = Client()
    client.login(username='testuser', password='testpassword')

    income, category, user = edit_monthly_income_list_view_negative

    form_data = {
        'value': 199
    }

    url = reverse('edit_monthly_income_list', kwargs={'pk': income.pk})
    response = client.post(url, data=form_data)

    assert response.status_code == 302

    income.refresh_from_db()
    assert income.value == -1000


# negative
@pytest.mark.django_db
def test_delete_monthly_income_list_view_positive(delete_monthly_income_list_view_positive):

    client = Client()
    client.login(username='testuser', password='testpassword')

    category, income, user = delete_monthly_income_list_view_positive

    url = reverse('delete_monthly_income_list', kwargs={'pk': income.pk})
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(url)

    assert response.status_code == 302

    assert Income.objects.filter(category='test category', value=1000, date='2023-12-23').exists()


# negative UNIQUE
@pytest.mark.django_db
def test_delete_monthly_income_list_view_negative(delete_monthly_income_list_view_negative):

    client = Client()
    client.login(username='testuser', password='testpassword')

    category, income, user = delete_monthly_income_list_view_negative

    url = reverse('delete_expense', kwargs={'pk': income.pk})
    response = client.get(url)

    assert response.status_code == 200

    invalid_form_data = {
        'value': 123,
        'category': 'test category',
        'date': '2023-12-23'
    }
    response = client.post(url, data=invalid_form_data)

    assert response.status_code == 200

    income.refresh_from_db()
    assert income.value == -1000


# negative UNIQUE
@pytest.mark.django_db
def test_edit_monthly_expenses_list_view_positive(edit_monthly_expenses_list_view_positive):

    client = Client()
    client.login(username='testuser', password='testpassword')
    category, expense, user = edit_monthly_expenses_list_view_positive

    url = reverse('edit_form', kwargs={'pk': expense.pk})
    response = client.get(url)

    assert response.status_code == 200

    updated_value = 600
    updated_form_data = {
        'value': updated_value,
    }
    response = client.post(url, data=updated_form_data)

    assert response.status_code == 302

    expense.refresh_from_db()
    assert expense.value == updated_value


# negative UNIQUE
@pytest.mark.django_db
def test_edit_monthly_expenses_list_view_negative(edit_monthly_expenses_list_view_negative):

    client = Client()
    client.login(username='testuser', password='testpassword')

    category, expense, user = edit_monthly_expenses_list_view_negative

    url = reverse('edit_monthly_expenses_list', kwargs={'pk': expense.pk})
    response = client.get(url)

    assert response.status_code == 302

    invalid_form_data = {
        'value': -100,
    }
    response = client.post(url, data=invalid_form_data)

    assert response.status_code == 200

    expense.refresh_from_db()
    assert expense.value == -500


# negative UNIQUE
@pytest.mark.django_db
def test_delete_monthly_expenses_list_view_positive(delete_monthly_expenses_list_view_positive):

    client = Client()
    client.login(username='testuser', password='testpassword')
    category, expense, user = delete_monthly_expenses_list_view_positive

    url = reverse('delete_form', kwargs={'pk': expense.pk})
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(url)

    assert response.status_code == 302

    assert Expenses.objects.filter(category='test category', value=1000, date='23-12-2023').exists()


# negative UNIQUE
@pytest.mark.django_db
def   test_delete_monthly_expenses_list_view_negative(delete_monthly_expenses_list_view_negative):

    client = Client()
    client.login(username='testuser', password='testpassword')
    category, expense, user = delete_monthly_expenses_list_view_negative

    url = reverse('delete_form', kwargs={'pk': expense.pk})
    response = client.get(url)

    assert response.status_code == 200

    response = client.post(url)

    assert response.status_code == 302

    assert Expenses.objects.filter(category='test category', value=-1000, date='23-12-2023').exists()
