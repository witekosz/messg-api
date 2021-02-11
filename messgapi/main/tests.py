from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from main.models import APIKey, Message


CONTENT_TYPE = "application/json"
TEST_API_KEY = "b8fd018e-6be3-11eb-9439-0242ac130002"
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


class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unauth_returns_401(self):
        response = self.client.post("/api/messages/", {"text": ""}, CONTENT_TYPE)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Unauthorized"})


class MessageBaseTest(TestCase):
    def setUp(self):
        APIKey.objects.create(key=TEST_API_KEY)
        Message.objects.create(text=TEXT_20)
        Message.objects.create(text=TEXT_40)

        self.client = Client(HTTP_X_API_Key=TEST_API_KEY)

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

    def test_get_increments_counter(self):
        existing_id = 2
        existing_counter = 5
        message = Message.objects.get(id=existing_id)
        message.counter = existing_counter
        message.save()
        self.assertEqual(Message.objects.get(id=existing_id).counter, existing_counter)

        response = self.client.get(f"/api/messages/{existing_id}/")
        response_data = response.json()

        self.assertEqual(response_data["counter"], existing_counter + 1)
        self.assertEqual(
            Message.objects.get(id=existing_id).counter, existing_counter + 1
        )

    def test_get_fails_returns_message(self):
        non_existing_id = 100

        response = self.client.get(f"/api/messages/{non_existing_id}/")
        response_data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Not found")


class MessageGETListTest(MessageBaseTest):
    def test_get_returns_messages_list(self):
        first_message_idx = 0
        objects_added = 2

        response = self.client.get("/api/messages/")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), objects_added)
        self.assertEqual(response_data[first_message_idx]["text"], TEXT_20)


class MessagePOSTTest(MessageBaseTest):
    def test_post_creates_message(self):
        response = self.client.post("/api/messages/", {"text": TEXT_60}, CONTENT_TYPE)
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["text"], TEXT_60)

    def test_post_fails_create_long_message(self):
        response = self.client.post("/api/messages/", {"text": TEXT_200}, CONTENT_TYPE)
        response_data = response.json()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response_data, {"message": "ensure text value has at most 160 characters"}
        )


class MessagePUTTest(MessageBaseTest):
    def test_put_update_message_and_reset_counter(self):
        existing_id = 1
        text_before_update = Message.objects.get(id=existing_id).text

        response = self.client.put(
            f"/api/messages/{existing_id}/", {"text": TEXT_60}, CONTENT_TYPE
        )
        response_data = response.json()
        text_after_update = Message.objects.get(id=existing_id).text

        self.assertEqual(text_before_update, TEXT_20)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["text"], TEXT_60)
        self.assertEqual(text_after_update, TEXT_60)

    def test_put_reset_counter(self):
        existing_id = 2
        existing_counter = 5
        zero_counter = 0
        message = Message.objects.get(id=existing_id)
        message.counter = existing_counter
        message.save()
        self.assertEqual(Message.objects.get(id=existing_id).counter, existing_counter)

        response = self.client.put(
            f"/api/messages/{existing_id}/", {"text": ""}, CONTENT_TYPE
        )
        response_data = response.json()

        self.assertEqual(response_data["counter"], zero_counter)
        self.assertEqual(Message.objects.get(id=existing_id).counter, zero_counter)

    def test_put_fails_update_message(self):
        non_existing_id = 100

        response = self.client.put(
            f"/api/messages/{non_existing_id}/", {"text": ""}, CONTENT_TYPE
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Not found")


class MessageDELETETest(MessageBaseTest):
    def test_delete_deletes_message(self):
        existing_id = 1
        objects_added = 2
        objects_before_delete = Message.objects.all().count()

        response = self.client.delete(f"/api/messages/{existing_id}/")
        objects_after_delete = Message.objects.all().count()

        self.assertEqual(objects_before_delete, objects_added)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(objects_after_delete, objects_added - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Message.objects.get(id=existing_id)

    def test_delete_fails_deletes_message(self):
        non_existing_id = 100

        response = self.client.delete(f"/api/messages/{non_existing_id}/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "Not found")
