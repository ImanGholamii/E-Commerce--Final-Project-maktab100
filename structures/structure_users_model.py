class CustomUserManager():
    """Custom manager for the User model.

    Methods:
        create_user(): Create a new user.
        create_superuser(): Create a new superuser.
    """


class User():
    """Custom User model.

    Attributes:
        username (str): The username of the user.
        user_type (str): The type of user (customer or employee).
        email (EmailField): The email address of the user.
        phone (str): The phone number of the user.
        gender (str): The gender of the user.
        date_of_birth (DateField): The date of birth of the user.
        registration_date (DateTimeField): The date and time the user registered.

    Manager:
        objects (CustomUserManager): Custom manager for the User model.
    """


class Employee():
    """Model representing an employee.

    Attributes:
        user (User): The user associated with the employee.
        role (str): The role of the employee (manager, staff, customer_support).
        is_manager (bool): Indicates whether the employee is a manager.
        is_staff (bool): Indicates whether the employee is staff.
        is_customer_support (bool): Indicates whether the employee is in customer support.
    """


class Customer():
    """Model representing a customer.

    Attributes:
        user (User): The user associated with the customer.
        profile_picture (ImageField): The profile picture of the customer.
        is_subscribed (bool): Indicates whether the customer is subscribed to news.
    """


class Address():
    """Model representing a user's address.

    Attributes:
        user (User): The user associated with the address.
        state (str): The state of the address.
        city (str): The city of the address.
        street (str): The street of the address.
        alley (str): The alley of the address.
        no (str): The number of the address.
        unit_number (str): The unit number of the address.
        postal_code (str): The postal code of the address.
        is_default (bool): Indicates whether the address is the default one.
        additional_info (str): Additional information about the address.
    """


class UserProfile():
    """Model representing a user's profile.

    Attributes:
        user (User): The user associated with the profile.
        bio (str): The biography of the user.
        social_media (str): The social media information of the user.
        interests (str): The interests of the user.
        addresses (ManyToManyField): The addresses associated with the user's profile.
    """
