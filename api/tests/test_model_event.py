from django.test import TestCase
from ..models import Event
from django.contrib.auth import get_user_model
User = get_user_model()


class EventTest(TestCase):
    """ Test module for Event model """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.user.save()
        Event.objects.create(
            user=self.user, application="Application 1", category="Error", severity=1, value="Er heeft een error plaatsgevonden")
        Event.objects.create(
            user=self.user, application="Application 2", category="Warning", severity=3, value="Er heeft een warning plaatsgevonden")

    def test_event(self):
        event1 = Event.objects.get(application='Application 1')
        event2 = Event.objects.get(application='Application 2')
        self.assertEqual(
            event1.category, "Error")
        self.assertEqual(
            event2.category, "Warning")