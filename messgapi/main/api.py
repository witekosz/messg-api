from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.responses import codes_4xx

from .auth import header_key
from .models import Message
from .schemas import (ErrorResponse, MessageResponse, MessageSend,
                      SuccessResponse)

api = NinjaAPI()


@api.get("/messages/", response=List[MessageResponse], tags=["messages"])
def get_messages(request):
    return Message.objects.all()


@api.get(
    "/messages/{message_id}/",
    response={200: MessageResponse, codes_4xx: ErrorResponse},
    tags=["messages"],
)
def get_message(request, message_id: int):
    try:
        message = Message.objects.get(pk=message_id)
    except ObjectDoesNotExist:
        return 404, {"message": "Not found"}

    message.counter += 1
    message.save()

    return 200, message


@api.post(
    "/messages/",
    response={200: MessageResponse, codes_4xx: ErrorResponse},
    auth=header_key,
    tags=["messages"],
)
def post_message(request, data: MessageSend):
    message = Message.objects.create(**data.dict())
    return 200, message


@api.put(
    "/messages/{message_id}/",
    response={200: MessageResponse, codes_4xx: ErrorResponse},
    auth=header_key,
    tags=["messages"],
)
def put_message(request, message_id: int, data: MessageSend):
    try:
        message = Message.objects.get(pk=message_id)
    except ObjectDoesNotExist:
        return 404, {"message": "Not found"}

    message.text = data.text
    message.counter = 0
    message.save()

    return 200, message


@api.delete(
    "/messages/{message_id}/",
    response={204: SuccessResponse, codes_4xx: ErrorResponse},
    auth=header_key,
    tags=["messages"],
)
def delete_message(request, message_id: int):
    try:
        message = Message.objects.get(pk=message_id)
    except ObjectDoesNotExist:
        return 404, {"message": "Not found"}

    message.delete()

    return 204, {"success": True}
