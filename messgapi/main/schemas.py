from ninja import Schema


class MessageSend(Schema):
    text: str


class MessageResponse(Schema):
    id: int
    counter: int
    text: str


class ErrorResponse(Schema):
    message: str


class SuccessResponse(Schema):
    success: bool
