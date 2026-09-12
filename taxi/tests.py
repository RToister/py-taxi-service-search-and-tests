from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class PublicPagesTests(TestCase):
    def test_login_required_for_index(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class SearchViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="search_driver",
            password="testpassword",
            license_number="ABC12345",
        )
        cls.other_driver = Driver.objects.create_user(
            username="another_driver",
            password="testpassword",
            license_number="DEF67890",
        )

        cls.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )
        cls.other_manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        cls.car = Car.objects.create(
            model="Model S",
            manufacturer=cls.manufacturer,
        )
        cls.other_car = Car.objects.create(
            model="Corolla",
            manufacturer=cls.other_manufacturer,
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_driver_search_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"name": "SEARCH"},
        )

        self.assertEqual(
            list(response.context["driver_list"]),
            [self.driver],
        )

    def test_car_search_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"name": "model"},
        )

        self.assertEqual(
            list(response.context["car_list"]),
            [self.car],
        )

    def test_manufacturer_search_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "tes"},
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [self.manufacturer],
        )

    def test_empty_search_returns_all_cars(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.context["car_list"].count(), 2)
