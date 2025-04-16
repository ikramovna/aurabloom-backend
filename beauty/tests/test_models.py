from django.test import TestCase

from beauty.models.about import *
from beauty.models.booking import *
from beauty.models.favorite import *
from beauty.models.region import *
from beauty.models.service import *
from users.models import User


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), "Test Category")

    def test_image_field(self):
        self.assertFalse(bool(self.category.image))


class ServiceModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user = User.objects.create(username="testuser", password="password123")
        self.service = Service.objects.create(
            name="Test Service",
            price=100.00,
            duration="30 mins",
            description="Test description",
            category=self.category,
            user=self.user,
            image=None
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Test Service")
        self.assertEqual(self.service.price, 100.00)
        self.assertEqual(self.service.duration, "30 mins")
        self.assertEqual(self.service.description, "Test description")
        self.assertEqual(self.service.category, self.category)
        self.assertEqual(self.service.user, self.user)
        self.assertFalse(bool(self.service.image))
        self.assertEqual(str(self.service), "Test Service")


class ShopModelTest(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(
            name="Test Shop",
            description="Test description",
            image=None,
            price=200.00,
            discount=20.00,
            view=10,
            availability=True,
            contact_number="1234567890",
            additional_info="Test additional info",
            brand="Test Brand",
            weight=1.5,
            size="Medium",
            grams=1500,
            color="Red"
        )

    def test_shop_creation(self):
        self.assertEqual(self.shop.name, "Test Shop")
        self.assertEqual(self.shop.description, "Test description")
        self.assertFalse(bool(self.shop.image))
        self.assertEqual(self.shop.price, 200.00)
        self.assertEqual(self.shop.discount, 20.00)
        self.assertEqual(self.shop.view, 10)
        self.assertTrue(self.shop.availability)
        self.assertEqual(self.shop.contact_number, "1234567890")
        self.assertEqual(self.shop.additional_info, "Test additional info")
        self.assertEqual(self.shop.brand, "Test Brand")
        self.assertEqual(self.shop.weight, 1.5)
        self.assertEqual(self.shop.size, "Medium")
        self.assertEqual(self.shop.grams, 1500)
        self.assertEqual(self.shop.color, "Red")
        self.assertEqual(str(self.shop), "Test Shop")


class BlogModelTest(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(
            title="Test Blog",
            description="Test description",
            image1=None,
            view=5
        )

    def test_blog_creation(self):
        self.assertEqual(self.blog.title, "Test Blog")
        self.assertEqual(self.blog.description, "Test description")
        self.assertFalse(bool(self.blog.image1))
        self.assertEqual(self.blog.view, 5)
        self.assertEqual(str(self.blog), "Test Blog")


class RegionModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Test Region")

    def test_region_creation(self):
        self.assertEqual(self.region.name, "Test Region")
        self.assertEqual(str(self.region), "Test Region")


class DistrictModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Test Region")
        self.district = District.objects.create(name="Test District", region=self.region)

    def test_district_creation(self):
        self.assertEqual(self.district.name, "Test District")
        self.assertEqual(self.district.region, self.region)
        self.assertEqual(str(self.district), "Test District")


class MahallaModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Test Region")
        self.district = District.objects.create(name="Test District", region=self.region)
        self.mahalla = Mahalla.objects.create(name="Test Mahalla", district=self.district)

    def test_mahalla_creation(self):
        self.assertEqual(self.mahalla.name, "Test Mahalla")
        self.assertEqual(self.mahalla.district, self.district)
        self.assertEqual(str(self.mahalla), "Test Mahalla")


class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password123")
        self.category = Category.objects.create(name="Test Category")
        self.service = Service.objects.create(
            name="Test Service",
            price=100.00,
            duration="30 mins",
            description="Test description",
            category=self.category,
            user=self.user,
            image=None
        )
        self.favorite = Favorite.objects.create(service=self.service, user=self.user, like=True)

    def test_favorite_creation(self):
        self.assertEqual(self.favorite.service, self.service)
        self.assertEqual(self.favorite.user, self.user)
        self.assertTrue(self.favorite.like)
        self.assertEqual(str(self.favorite), f"{self.user.username} - {self.service.name}")

    def test_get_favorites(self):
        favorites = Favorite.get_favorites(self.user)
        self.assertIn(self.favorite, favorites)

    def test_get_total_likes(self):
        total_likes = Favorite.get_total_likes()
        self.assertEqual(total_likes, 1)


class SavedModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password123")
        self.category = Category.objects.create(name="Test Category")
        self.service = Service.objects.create(
            name="Test Service",
            price=100.00,
            duration="30 mins",
            description="Test description",
            category=self.category,
            user=self.user,
            image=None
        )
        self.saved = Saved.objects.create(service=self.service, user=self.user, saved=True)

    def test_saved_creation(self):
        self.assertEqual(self.saved.service, self.service)
        self.assertEqual(self.saved.user, self.user)
        self.assertTrue(self.saved.saved)
        self.assertEqual(str(self.saved), f"{self.user.username} - {self.service.name}")


class ShopFavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password123")
        self.shop = Shop.objects.create(
            name="Test Shop",
            description="Test description",
            image=None,
            price=200.00,
            discount=20.00,
            view=10,
            availability=True
        )
        self.shop_favorite = ShopFavorite.objects.create(product=self.shop, user=self.user, like=True)

    def test_shop_favorite_creation(self):
        self.assertEqual(self.shop_favorite.product, self.shop)
        self.assertEqual(self.shop_favorite.user, self.user)
        self.assertTrue(self.shop_favorite.like)
        self.assertEqual(str(self.shop_favorite), f"{self.user.username} - {self.shop.name}")


class ShopSavedModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password123")
        self.shop = Shop.objects.create(
            name="Test Shop",
            description="Test description",
            image=None,
            price=200.00,
            discount=20.00,
            view=10,
            availability=True
        )
        self.shop_saved = ShopSaved.objects.create(product=self.shop, user=self.user, saved=True)

    def test_shop_saved_creation(self):
        self.assertEqual(self.shop_saved.product, self.shop)
        self.assertEqual(self.shop_saved.user, self.user)
        self.assertTrue(self.shop_saved.saved)
        self.assertEqual(str(self.shop_saved), f"{self.user.username} - {self.shop.name}")


class WorkingDaysModelTest(TestCase):
    def setUp(self):
        self.working_day = WorkingDays.objects.create(day="Monday")

    def test_working_day_creation(self):
        self.assertEqual(self.working_day.day, "Monday")
        self.assertEqual(str(self.working_day), "Monday")


class TimeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password123")
        self.working_day = WorkingDays.objects.create(day="Monday")
        self.time = Time.objects.create(
            day=self.working_day,
            start_time="09:00",
            end_time="17:00",
            user=self.user
        )

    def test_time_creation(self):
        self.assertEqual(self.time.day, self.working_day)
        self.assertEqual(self.time.start_time, "09:00")
        self.assertEqual(self.time.end_time, "17:00")
        self.assertEqual(self.time.user, self.user)
        self.assertEqual(str(self.time), "Monday 09:00 - 17:00")


class FaqModelTest(TestCase):
    def setUp(self):
        self.faq = Faq.objects.create(
            question="What is your return policy?",
            answer="You can return items within 30 days."
        )

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "What is your return policy?")
        self.assertEqual(self.faq.answer, "You can return items within 30 days.")
        self.assertEqual(str(self.faq), "What is your return policy?")


class AboutModelTest(TestCase):
    def setUp(self):
        self.about_image = AboutImage.objects.create(image=None)
        self.about = About.objects.create(
            title="About Our Company",
            description="We are a company dedicated to excellence."
        )
        self.about.image.add(self.about_image)

    def test_about_creation(self):
        self.assertEqual(self.about.title, "About Our Company")
        self.assertEqual(self.about.description, "We are a company dedicated to excellence.")
        self.assertIn(self.about_image, self.about.image.all())
        self.assertEqual(str(self.about), "About Our Company")


class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            full_name="John Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            message="I would like to know more about your services."
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.full_name, "John Doe")
        self.assertEqual(self.contact.email, "johndoe@example.com")
        self.assertEqual(self.contact.phone_number, "1234567890")
        self.assertEqual(self.contact.message, "I would like to know more about your services.")
