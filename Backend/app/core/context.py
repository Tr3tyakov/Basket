from dataclasses import dataclass
from typing import Optional

from starlette.requests import Request

from app.core.database import Database


@dataclass
class ApplicationContext:
    database: Optional[Database] = None

    @staticmethod
    async def get_context(request: Request) -> "ApplicationContext":
        return request.app.extra["context"]
