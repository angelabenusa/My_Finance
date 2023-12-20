"""
URL configuration for diploma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MyFinance import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('', views.HomePageAccountBalanseView.as_view(), name='homepage_with_account_balance'),
    path('add_category_income/', views.AddCategoryIncomeView.as_view(), name='add_category_income'),
    path('category_income_list/', views.CategoryIncomeListView.as_view(), name='category_income_list'),
    path('add_category_expenses/', views.AddCategoryExpensesView.as_view(), name='add_category_expenses'),
    path('category_income_list/<int:pk>/edit/', views.EditCategoryIncomeListView.as_view(), name='edit_category_income_list'),
    path('category_income_list/<int:pk>/delete/',views.DeleteCategoryIncomeListView.as_view(), name='delete_category_income_list'),
    path('category_expenses_list/', views.CategoryExpensesListView.as_view(), name='category_expenses_list'),
    path('category_expenses_list/<int:pk>/edit/', views.EditCategoryExpensesListView.as_view(), name='edit_category_expenses_list'),
    path('category_expenses_list/<int:pk>/delete/', views.DeleteCategoryExpensesListView.as_view(), name='delete_category_expenses_list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact_message/<str:name>/<str:email>/', views.ContactMessageView.as_view(), name='contact_message'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('base/', TemplateView.as_view(template_name='base.html'), name='base'),
    path('monthly_expenses_list/', views.MonthlyExpensesListView.as_view(), name='monthly_expenses_list'),
    path('monthly_income_list/', views.MonthlyIncomeListView.as_view(), name='monthly_income_list'),
    path('detailed_category_expenses_list/<int:category_id>/', views.DetailedCategoryExpensesListView.as_view(), name='detailed_category_expenses_list'),
    path('detailed_category_income_list/<int:category_id>/', views.DetailedCategoryIncomeListView.as_view(), name='detailed_category_income_list'),
    path('wallets/', views.ShowWalletsView.as_view(), name='wallets'),
    path('wallet/<int:pk>/edit/', views.EditWalletView.as_view(), name='edit_wallet'),
    path('wallet/<int:pk>/delete/', views.DeleteWalletView.as_view(), name='delete_wallet'),
    path('add_income_expenses_to_wallet/<int:wallet_id>/', views.AddIncomeExpensesToWalletView.as_view(), name='add_income_expense_to_wallet'),
    path('add_income_to_wallet/<int:wallet_id>/', views.AddIncomeToWalletView.as_view(), name='add_income_to_wallet'),
    path('add_expenses_to_wallet/<int:wallet_id>/', views.AddExpensesToWalletView.as_view(), name='add_expenses_to_wallet'),

    path('add_income_expenses_to_wallet/<int:pk>/edit/', views.EditAddIncomeToWalletView.as_view(), name='edit_add_income_to_wallet'),
    path('add_income_expenses_to_wallet/edit/<int:pk>/', views.EditAddExpensesToWalletView.as_view(), name='edit_add_expenses_to_wallet'),
    path('add_income_expenses_to_wallet/<int:pk>/delete/', views.DeleteAddIncomeToWalletView.as_view(), name='delete_add_income_to_wallet'),
    path('add_income_expenses_to_wallet/delete/<int:pk>/', views.DeleteAddExpensesToWalletView.as_view(), name='delete_add_expenses_to_wallet'),

    path('monthly_income_list/<int:pk>/edit/', views.EditMonthlyIncomeListView.as_view(), name='edit_monthly_income_list'),
    path('monthly_income_list/<int:pk>/delete/', views.DeleteMonthlyIncomeListView.as_view(), name='delete_monthly_income_list'),
    path('monthly_expenses_list/<int:pk>/edit/', views.EditMonthlyExpensesListView.as_view(), name='edit_monthly_expenses_list'),
    path('monthly_expenses_list/<int:pk>/delete/', views.DeleteMonthlyExpensesListView.as_view(), name='delete_monthly_expenses_list')
    ]
