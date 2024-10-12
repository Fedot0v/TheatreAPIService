from unittest import TestCase

from django.urls import reverse


TICKET_URL = reverse("theatre:ticket-list")


class UnAuthenticatedTest(TestCase):
    def setUp(self):
        self.client = 