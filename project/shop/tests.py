from django import forms
from django.db import models
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse

from shop.forms import BootstrapFieldsMixin
from shop.models import TimeStampedModel
from shop.templatetags.shop.filters import times


class ShopViewTest(TestCase):
    """
    Tests for Shop Views and Mixins.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("shop_page")

    def test_shop_page_view(self):
        """Test that the home page loads correctly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/index.html")

        # Check context from BaseContextMixin
        self.assertEqual(response.context["page_name"], "Home")
        # Breadcrumbs are empty for home page in your view logic
        self.assertEqual(response.context["breadcrumbs"], [])


class ShopFormTest(SimpleTestCase):
    """
    Tests for the BootstrapFieldsMixin in forms.py.
    """

    def setUp(self):
        # Define a dummy form using the mixin
        class TestForm(BootstrapFieldsMixin, forms.Form):
            text_field = forms.CharField(required=True)
            checkbox_field = forms.BooleanField(required=False)

        self.TestForm = TestForm

    def test_bootstrap_classes_applied(self):
        """Test that form-control and form-check-input classes are added."""
        form = self.TestForm()

        # Check text field for 'form-control'
        self.assertIn('class="form-control"', str(form['text_field']))

        # Check checkbox for 'form-check-input'
        self.assertIn('class="form-check-input"', str(form['checkbox_field']))

    def test_is_invalid_class_on_error(self):
        """Test that 'is-invalid' class is added when field has errors."""
        # Bind empty data to trigger required error on text_field
        form = self.TestForm(data={})

        self.assertFalse(form.is_valid())

        # text_field should have error and thus 'is-invalid' class
        self.assertIn('is-invalid', form['text_field'].field.widget.attrs['class'])
        self.assertIn('form-control', form['text_field'].field.widget.attrs['class'])


class ShopFilterTest(SimpleTestCase):
    """
    Tests for custom template filters (templatetags/shop/filters.py).
    """

    def test_times_filter(self):
        """Test the times filter returns correct range."""
        # range(0, 5)
        self.assertEqual(list(times(5)), [0, 1, 2, 3, 4])

    def test_times_filter_with_start(self):
        """Test the times filter with a start offset."""
        # range(1, 6) -> start=1, end=5 -> range(1, 5+1)
        self.assertEqual(list(times(5, 1)), [1, 2, 3, 4, 5])


class ShopModelTest(TestCase):
    """
    Tests for the TimeStampedModel (Abstract).
    """

    def test_abstract_model_inheritance(self):
        """
        Verify that TimeStampedModel is abstract and has correct fields.
        We cannot instantiate it directly, but we can check its meta options
        and field existence via a concrete implementation or inspection.
        """
        self.assertTrue(TimeStampedModel._meta.abstract)

        field_names = [f.name for f in TimeStampedModel._meta.fields]
        self.assertIn('created_at', field_names)
        self.assertIn('updated_at', field_names)