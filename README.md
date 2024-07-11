# My Finance

## Overview

My Finance is a Django-based web application designed to help users manage their home budgets effectively. Users can track their income, expenses, and manage multiple wallets to keep their finances organized.

## Features

- User Authentication (Login, Logout, Registration)
- Manage Categories for Income and Expenses
- Add and Track Incomes and Expenses
- Filter Incomes and Expenses
- Manage Multiple Wallets
- Transfer funds between wallets
- Contact form for user feedback

## Setup and Installation

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Virtualenv (optional but recommended)

### Installation Steps

1. Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/myfinance.git](https://github.com/angelabenusa/My_Finance.git)
    cd myfinance
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://127.0.0.1:8000`.
