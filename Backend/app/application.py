from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.context import ApplicationContext
from app.core.database import Database
from app.routers import ROUTERS


class Application:
    def __init__(self):
        self.app = FastAPI(lifespan=self.lifespan)
        self.database = Database(settings.POSTGRES)

    @asynccontextmanager
    async def lifespan(self, _):
        self.database._connect()
        yield
        await self.database._close()

    def _init_context(self) -> ApplicationContext:
        """Инициализация контекста сервиса"""
        return ApplicationContext(database=self.database)

    def _add_middlewares(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://127.0.0.1:5500",
            ],
            allow_credentials=True,
            allow_methods=["GET", "POST", "DELETE"],
            allow_headers=["*"],
        )

    def _add_routers(self) -> None:
        """Добавление роутеров"""
        for router in ROUTERS:
            self.app.include_router(router)

    def init_app(self) -> FastAPI:
        self._add_middlewares()
        self._add_routers()
        self.app.extra["context"] = self._init_context()
        return self.app


app = Application().init_app()
