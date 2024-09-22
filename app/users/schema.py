from typing import Optional, Self

from flask_restful import abort
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    field_validator,
    model_validator,
)
from typing_extensions import Annotated

from app.validators import (
    check_passwords_match,
    validate_email,
    validate_password,
    validate_username,
)


class UserRegisterSchema(BaseModel):
    username: Annotated[str, BeforeValidator(validate_username)]
    email: Annotated[str, BeforeValidator(validate_email)]
    password: Annotated[str, BeforeValidator(validate_password)]
    confirm_password: Annotated[str, BeforeValidator(validate_password)]

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if not check_passwords_match(self.password, self.confirm_password):
            abort(400, message="passwords do not match")
        return self

    model_config = ConfigDict(
        extra="allow",
    )


class UserLoginSchema(BaseModel):
    email: Annotated[str, BeforeValidator(validate_email)]
    password: Annotated[str, BeforeValidator(validate_password)]


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
