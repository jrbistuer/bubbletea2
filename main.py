from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routing.bubbletea import router as bubbletea_router

app = FastAPI(title="BubbleTea API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bubbletea_router)

@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    return {"status": "ok"}
