import json
from typing import Any, Generic, Optional, TypeVar

from fastapi import Response
from fastapi.encoders import jsonable_encoder   
from pydantic import BaseModel

T = TypeVar("T")

class BaseResponseModel(BaseModel, Generic[T]):
    status_code: int
    msg: str
    data: Optional[T] = None

    @staticmethod
    def succeed(status_code: int = 200, msg: str = "succeed", data: Any = None) -> Response:
        content = {"status_code": status_code, "msg": msg, "data": data}

        json_compatible = jsonable_encoder(content)

        return Response(
            status_code=status_code,
            content=json.dumps(json_compatible),
            media_type="application/json",
        )

    @staticmethod
    def failed(
        status_code: int = 500, msg: str = "failed", data: Any = None
    ) -> Response:
        content = {"status_code": status_code, "msg": msg, "data": data}

        json_compatible = jsonable_encoder(content)

        return Response(
            status_code=status_code,
            content=json.dumps(json_compatible),
            media_type="application/json",
        )
