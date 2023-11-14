from starlette.types import ASGIApp, Receive, Scope, Send
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger
from scheduler.scheduler import clean_expired_files


class SchedulerMiddlerware:
    def __init__(
        self,
        app: ASGIApp,
        scheduler: AsyncScheduler,
    ) -> None:
        self.app = app
        self.scheduler = scheduler

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            async with self.scheduler:
                # Add your tasks
                await self.scheduler.add_schedule(
                    clean_expired_files,
                    IntervalTrigger(days=1),
                    id="clean_expired_files",
                )
                
                await self.scheduler.start_in_background()
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)
