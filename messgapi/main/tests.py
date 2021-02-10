from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test import Client

from main.models import Message


CONTENT_TYPE = "application/json"
TEXT_20 = "Lorem ipsum posuere."
TEXT_40 = "Lorem ipsum dolor sit amet orci aliquam."
TEXT_60 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit est."
TEXT_160 = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Phasellus gravida, turpis sed convallis egestas, magna augue ullamcorper urna,
    non pulvinar lacus eget.
"""
TEXT_200 = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Praesent at mauris in ante rhoncus iaculis volutpat non nibh.
    Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere blandit.
"""


class MessageBaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        Message.objects.create(text=TEXT_20)
        Message.objects.create(text=TEXT_40)

    def tearDown(self):
        Message.objects.all().delete()


class MessageGETDetailsTest(MessageBaseTest):
    def test_get_returns_message(self):
        existing_id = 1

        response = self.client.get(f"/api/messages/{existing_id}/")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 3)
        self.assertEqual(response_data["text"], TEXT_20)


class MessageGETListTest(MessageBaseTest):
    def test_get_returns_messages_list(self):
        first_message_idx = 1

        response = self.client.get("/api/messages/")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 3)
        self.assertEqual(response_data["text"][first_message_idx], TEXT_20)


class MessagePOSTTest(MessageBaseTest):
    def test_post_creates_message(self):
        response = self.client.post(
            "/api/messages/", {"text": TEXT_60}, CONTENT_TYPE
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], TEXT_60)


class MessagePUTTest(MessageBaseTest):
    def test_put_updates_message(self):
        existing_id = 1
        text_before_update = Message.objects.get(id=existing_id).text

        response = self.client.put(
            f"/api/messages/{existing_id}/", {"text": TEXT_60}, CONTENT_TYPE
        )
        text_after_update = Message.objects.get(id=existing_id).text

        self.assertEqual(text_before_update, TEXT_20)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], TEXT_60)
        self.assertEqual(text_after_update, TEXT_60)


class MessageGETTest(MessageBaseTest):
    def test_delete_deletes_messages(self):
        existing_id = 1
        objects_added = 2
        objects_before_delete = Message.objects.all().count()

        response = self.client.delete(f"/api/messages/{existing_id}/")
        objects_after_delete = Message.objects.all().count()

        self.assertEqual(objects_before_delete, objects_added)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(objects_after_delete, objects_added - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Message.objects.get(id=existing_id)
