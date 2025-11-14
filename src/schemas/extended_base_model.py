from pydantic import BaseModel


class ExtendedBaseModel(BaseModel):
    model_config = {"extra": "ignore"}
