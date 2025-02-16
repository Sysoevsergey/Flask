from pydantic import BaseModel, field_validator, ValidationError
from errors import HttpError


class BaseUser(BaseModel):
    username: str
    password: str

    @field_validator('password')
    @classmethod
    def secure_password(cls, val: str):
        if len(val) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return val


class CreateUser(BaseUser):
   ...


class UpdateUser(BaseModel):
    username: str | None = None
    password: str | None = None

SCHEMA =type [CreateUser] | type [UpdateUser]

def validate(cls_schema: SCHEMA, json_data: dict):
    try:
        schema = cls_schema(**json_data)
        return schema.dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)
