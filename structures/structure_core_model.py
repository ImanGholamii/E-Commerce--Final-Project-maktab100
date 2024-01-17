class TimeStampBaseModel():
    """Abstract base model for adding timestamp information to models.

    Attributes:
        created_at (DateTime): The timestamp indicating when the record was created.
        updated_at (DateTime): The timestamp indicating when the record was last modified.

    Meta:
        abstract = True
    """


class LogicalQuerySet():
    """Custom queryset for logical deletion.

    Methods:
        delete(): Logically delete objects by setting is_deleted to True.
        hard_delete(): Physically delete objects from the database.
    """

    def delete(self):
        pass

    def hard_delete(self):
        pass


class LogicalManager():
    """Custom manager for handling logical deletion.

    Methods:
        get_queryset(): Get the queryset for active, non-deleted objects.
        all_objects(): Get the queryset for all objects, including deleted ones.
        deleted(): Get the queryset for only deleted objects.
    """


class LogicalBaseModel():
    """Abstract base model for adding logical deletion to models.

    Attributes:
        is_active (bool): Indicates whether the record is active or not.
        is_deleted (bool): Indicates whether the record has been logically deleted.

    Manager:
        objects (LogicalManager): Custom manager for handling logical deletion.

    Meta:
        abstract = True

    Methods:
        delete(): Logically delete the object by setting is_deleted to True.
        hard_delete(): Physically delete the object from the database.
        restore(): Restore a logically deleted object by setting is_deleted to False.
    """

    def delete(self):
        """Logically delete the object by setting is_deleted to True."""

    def hard_delete(self):
        """Physically delete the object from the database."""

    def restore(self):
        """Restore a logically deleted object by setting is_deleted to False."""
