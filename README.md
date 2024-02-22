# Final-Project-m100
In this project, we intend to design a store website

# Online Store

This project is a web-based online store aiming to handle all operations of a retail store online. The store encompasses functionalities such as managing customers, products, orders, and various categories.

## Features

- **Product Management:** Administrators and staff can add, edit, or remove products. Additionally, products have their categories and can be subject to discounts.
- **Shopping Cart:** Customers can add desired products to their shopping cart and place orders by selecting an address. Each order can comprise multiple products with varying quantities.
- **Order Management:** Staff can view order statuses, record order dates, and manage delivery timelines.
- **Customer Dashboard:** Customers can view their order statuses, check their order history, and edit their account information.
- **API Provision:** The project offers an API that provides store functionalities to other systems.

## Technologies Used

- **Python/Django:** The backend of this website is implemented using the Django framework.
- **PostgreSQL:** The system's database is managed using PostgreSQL.
- **Frontend:** jQuery, Bootstrap, JS, CSS, and HTML are used for design and user interface.

## Setting Up the Project

To set up the project, ensure Python and PostgreSQL are installed. Then, you can use the following commands to clone and run the project:

```bash
git clone https://github.com/ImanGholamii/Final-Project-m100.git
cd Final-Project-m100
env MODE=production pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
