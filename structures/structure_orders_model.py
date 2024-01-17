class Order():
    """Model representing an order.

    Attributes:
        products (Product): The products in the order.
        employee (Employee): The employee assigned to the order.
        customer (Customer): The customer placing the order.
        order_date (DateTime): The date and time the order was placed.
        status (str): The status of the order (pending, processing, completed, cancelled).

    Methods:
        __str__(): String representation of the order.
        calculate_total_price(): Calculate the total price of the order.
    """


class OrderItem():
    """Model representing an item in an order.

    Attributes:
        product (Product): The product in the order item.
        order (Order): The order to which the item belongs.
        quantities (int): The quantity of the product in the order item.

    Methods:
        __str__(): String representation of the order item.
    """


class OrderHistory():
    """Model representing the history of an order.

    Attributes:
        order (Order): The order for which the history is recorded.
        customer (Customer): The customer associated with the order history.
        status (str): The status of the order at the recorded time.
        time (DateTime): The date and time the history entry was created.
        modified (DateTime): The date and time the history entry was last modified.

    Methods:
        __str__(): String representation of the order history.
    """
