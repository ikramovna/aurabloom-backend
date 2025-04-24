from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from beauty.models.about import Faq, About, AboutImage, Contact
from beauty.models.booking import Booking, WorkingDays
from beauty.serializers.about import (
    FaqModelSerializer,
    AboutImageModelSerializer,
    AboutModelSerializer,
    ContactModelSerializer,
)
from beauty.serializers.booking import (
    WorkingDaySerializer,
    BookingUpdateSerializer,
)
from users.models import User


class FaqModelSerializerTest(APITestCase):
    def setUp(self):
        self.faq = Faq.objects.create(
            question="What is your return policy?",
            answer="You can return items within 30 days."
        )
        self.serializer = FaqModelSerializer(instance=self.faq)

    def test_faq_serialization(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.faq.id)
        self.assertEqual(data['question'], self.faq.question)
        self.assertEqual(data['answer'], self.faq.answer)


class AboutImageModelSerializerTest(APITestCase):
    def setUp(self):
        self.about_image = AboutImage.objects.create(image=None)
        self.serializer = AboutImageModelSerializer(instance=self.about_image)

    def test_about_image_serialization(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.about_image.id)
        self.assertEqual(data['image'], self.about_image.image)


class AboutModelSerializerTest(APITestCase):
    def setUp(self):
        self.about_image = AboutImage.objects.create(image=None)
        self.about = About.objects.create(
            title="About Our Company",
            description="We are a company dedicated to excellence."
        )
        self.about.image.add(self.about_image)
        self.serializer = AboutModelSerializer(instance=self.about)

    def test_about_serialization(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.about.id)
        self.assertEqual(data['title'], self.about.title)
        self.assertEqual(data['description'], self.about.description)
        self.assertEqual(len(data['image']), 1)
        self.assertEqual(data['image'][0]['id'], self.about_image.id)


class ContactModelSerializerTest(APITestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            full_name="John Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            message="I would like to know more about your services."
        )
        self.serializer = ContactModelSerializer(instance=self.contact)

    def test_contact_serialization(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.contact.id)
        self.assertEqual(data['full_name'], self.contact.full_name)
        self.assertEqual(data['email'], self.contact.email)
        self.assertEqual(data['phone_number'], self.contact.phone_number)
        self.assertEqual(data['message'], self.contact.message)


class WorkingDaySerializerTest(APITestCase):
    def setUp(self):
        self.working_day = WorkingDays.objects.create(day="Monday")
        self.serializer = WorkingDaySerializer(instance=self.working_day)

    def test_working_day_serialization(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.working_day.id)
        self.assertEqual(data['day'], self.working_day.day)


class BookingUpdateSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password123")
        self.booking = Booking.objects.create(
            date=(timezone.now() + timedelta(days=1)).date(),
            time="10:00",
            user=self.user,
            status=Booking.StatusChoices.PENDING
        )
        self.serializer = BookingUpdateSerializer(instance=self.booking)

    def test_booking_update_validation(self):
        serializer = BookingUpdateSerializer(instance=self.booking, data={"status": Booking.StatusChoices.APPROVED})
        self.assertTrue(serializer.is_valid())
        updated_booking = serializer.update(self.booking, serializer.validated_data)
        self.assertEqual(updated_booking.status, Booking.StatusChoices.APPROVED)
