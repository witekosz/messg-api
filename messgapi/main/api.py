from typing import List

from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from main.models import Message


api = NinjaAPI()


class MessageSend(Schema):
    text: str


class MessageResponse(Schema):
    id: int
    counter: int
    text: str


@api.get("/messages/", response=List[MessageResponse], tags=["messages"])
def get_messages(request):
    return Message.objects.all()


@api.get("/messages/{message_id}/", response=MessageResponse, tags=["messages"])
def get_message(request, message_id: int):
    message = get_object_or_404(Message, id=message_id)
    message.counter += 1
    message.save()
    return message


@api.post("/messages/", response=MessageResponse, tags=["messages"])
def post_message(request, data: MessageSend):
    message = Message.objects.create(**data.dict())
    return message


@api.put("/messages/{message_id}/", response=MessageResponse, tags=["messages"])
def put_message(request, message_id: int, data: MessageSend):
    message = get_object_or_404(Message, id=message_id)
    message.text = data.text
    message.counter = 0
    message.save()
    return message


@api.delete("/messages/{message_id}/", tags=["messages"])
def delete_message(request, message_id: int):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return {"success": True}
