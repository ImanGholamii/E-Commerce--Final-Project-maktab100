class ProductImageAlbum():
    """Model representing a collection of product images.

    Attributes:
        image (ImageField): The main image file.
        is_default (bool): Indicates if this image is the default for the product.

    Properties:
        url (str): The URL of the image.

    Methods:
        __str__(): String representation of the product image album.
    """


class ProductImages():
    """Model representing individual product images associated with a specific product.

    Attributes:
        product (Product): The product to which the image belongs.
        image (ProductImageAlbum): The image album to which the image belongs.

    Methods:
        __str__(): String representation of the product image.
    """
