from fastapi import FastAPI

from src.domains.auction.api import bid_routers

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    from storage.db_config import init_db
    await init_db()

from src.domains.auction.containers import UseCaseContainer

use_case_container = UseCaseContainer()
use_case_container.wire(packages=[bid_routers])

app.include_router(bid_routers.bid_router)
