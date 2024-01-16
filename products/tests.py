from django.conf import settings
from django.test import TestCase
from products.models import Brand, Category


class BaseModelTest(TestCase):
    def assertBaseModelProperties(self, model_instance):
        """Test properties/methods inherited from LogicalBaseModel"""
        self.assertTrue(hasattr(model_instance, 'is_active'))
        self.assertTrue(hasattr(model_instance, 'is_deleted'))
        self.assertTrue(hasattr(model_instance, 'delete'))
        self.assertTrue(hasattr(model_instance, 'hard_delete'))
        self.assertTrue(hasattr(model_instance, 'restore'))

    def assertTimeStampBaseModelProperties(self, model_instance):
        """Test properties/methods inherited from TimeStampBaseModel"""
        self.assertTrue(hasattr(model_instance, 'created_at'))
        self.assertTrue(hasattr(model_instance, 'updated_at'))


class BrandModelTest(BaseModelTest):
    def setUp(self):
        """Create a sample Brand instance for testing"""
        self.brand = Brand.objects.create(
            name='Test Brand',
            description='This is a test brand'
        )

    def test_str_method(self):
        """Test the __str__ method for proper string representation"""
        self.assertEqual(str(self.brand), 'Test Brand')

    def test_base_model_properties(self):
        self.assertBaseModelProperties(self.brand)

    def test_timestamp_base_model_properties(self):
        self.assertTimeStampBaseModelProperties(self.brand)

    def test_name_max_length(self):
        """Test that the name field has the correct max length"""
        max_length = self.brand._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_verbose_name(self):
        """Test verbose names for fields"""
        name_field = self.brand._meta.get_field('name')
        description_field = self.brand._meta.get_field('description')

        self.assertEqual(name_field.verbose_name, 'Name')
        self.assertEqual(description_field.verbose_name, 'Description')


class CategoryModelTest(BaseModelTest):
    """Test case for the Category model."""

    def setUp(self):
        """Set up sample Category instances for testing."""
        self.parent_category = Category.objects.create(
            name='Parent Category',
            description='This is a parent category',
            image='category_images/parent_image.jpg',
        )

        self.category = Category.objects.create(
            name='Test Category',
            description='This is a test category',
            image='category_images/test_image.jpg',
            parent=self.parent_category,
        )

    def test_str_method(self):
        """Test the __str__ method for proper string representation."""
        self.assertEqual(str(self.category), 'Test Category')

    def test_base_model_properties(self):
        """Test properties/methods inherited from LogicalBaseModel."""
        self.assertBaseModelProperties(self.category)

    def test_timestamp_base_model_properties(self):
        """Test properties/methods inherited from TimeStampBaseModel."""
        self.assertTimeStampBaseModelProperties(self.category)

    def test_name_max_length(self):
        """Test that the name field has the correct max length."""
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_verbose_name(self):
        """Test verbose names for fields."""
        name_field = self.category._meta.get_field('name')
        description_field = self.category._meta.get_field('description')
        image_field = self.category._meta.get_field('image')
        parent_field = self.category._meta.get_field('parent')

        self.assertEqual(name_field.verbose_name, 'Name')
        self.assertEqual(description_field.verbose_name, 'Description')
        self.assertEqual(image_field.verbose_name, 'Image')
        self.assertEqual(parent_field.verbose_name, 'Parent')

    def test_parent_relationship(self):
        """Test the parent-child relationship."""
        self.assertEqual(self.category.parent, self.parent_category)
        self.assertEqual(list(self.parent_category.child.all()), [self.category])

    def test_get_full_path_no_parent(self):
        """Test the get_full_path method when the category has no parent."""
        self.parent_category.parent = None
        self.parent_category.save()

    def test_create_category_without_parent(self):
        """Test creating a category without a parent."""
        new_category = Category.objects.create(
            name='New Category',
            description='This is a new category',
            image='path/to/new_image.jpg',
        )
        self.assertIsNone(new_category.parent)

    def test_get_full_path(self):
        """Test the get_full_path method."""
        expected_path = 'Parent Category > Test Category'
        actual_path = self.category.get_full_path()
        self.assertEqual(actual_path, expected_path)

    def test_image_upload_path(self):
        """Test that the image is uploaded to the correct path."""
        expected_path = 'category_images/test_image.jpg'
        media_root = settings.MEDIA_ROOT

        actual_path = self.category.image.path[len(media_root) + 1:]

        self.assertEqual(actual_path, expected_path)

        expected_path = 'Parent Category'
        actual_path = self.parent_category.get_full_path()
        self.assertEqual(actual_path, expected_path)

    def test_image_upload_to(self):
        """Test the correct upload path for the ImageField."""
        image_field = self.category._meta.get_field('image')
        self.assertEqual(image_field.upload_to, 'category_images/')

    def test_restore_category(self):
        """Test the restore method."""
        self.category.delete()
        self.category.restore()
        self.assertTrue(self.category.is_active)

    def test_hard_delete_category(self):
        """Test the hard_delete method."""
        self.category.hard_delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=self.category.pk)
