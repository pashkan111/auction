from fastapi import FastAPI

from src.domains.auction.api.bid_routers import bid_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    from storage.db_config import init_db
    await init_db()


app.include_router(bid_router)
