class Brand():
    """Model representing a brand
    Attributes:
    name, description
    """


class Category():
    """Model representing a category
    Attributes:
        parent, image, description, name

    Methods:
    get_full_path():get parent of current category
    """


class Product():
    """Model representing a product.

        Attributes:
            name (str): The name of the product.
            description (str): A description of the product.
            category (Category): The category or categories to which the product belongs.
            price (Decimal): The price of the product.
            brand (Brand): The brand of the product, if any.

        Methods:
            __str__(): String representation of the product.
        """


class ProductCategory():
    """Model representing the relationship between products and categories.

        Attributes:
            product (Product): The product in the relationship.
            category (Category): The category in the relationship.

        Meta:
            db_table (str): Custom name for the database table.
        """


class Discount():
    """Model representing a discount for a product.

        Attributes:
            product (Product): The product to which the discount applies.
            discount_type (str): Type of discount ('percentage' or 'fixed').
            value (Decimal): The value of the discount.
            max_amount (Decimal): The maximum amount the discount can be.

        Methods:
            __str__(): String representation of the discount.
        """


class PromoCode():
    """Model representing a promo code for a discount.

        Attributes:
            discount (Discount): The discount associated with the promo code.
            code (str): The promo code.
            valid_from (DateTime): The start date and time of the promo code's validity.
            valid_to (DateTime): The end date and time of the promo code's validity.

        Methods:
            __str__(): String representation of the promo code.
            clean(): Validation method to ensure valid_from is before valid_to.
        """


class Comment():
    """Model representing a user comment on a product.

        Attributes:
            user (User): The user who made the comment.
            content (str): The content of the comment.
            product (Product): The product being commented on.
        """


class ParentChildComment():
    """Model representing the relationship between parent and child comments.

        Attributes:
            parent (Comment): The parent comment.
            child (Comment): The child comment.
            depth (int): The depth of the relationship.

        Meta:
            unique_together (tuple): Ensure uniqueness of parent and child combination.
        """
