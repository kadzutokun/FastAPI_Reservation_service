import uvicorn
from fastapi import FastAPI
from src.reservations.router import router as reservations_router
from src.users.router import router as users_router
from src.events.router import router as events_router
from fastapi.middleware.cors import CORSMiddleware
from src.core.transaction_middleware import TransactionMiddleware

app = FastAPI(title="Bookings reservation App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TransactionMiddleware)

app.include_router(reservations_router, prefix="/reservations", tags=["Reservations"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(events_router, prefix="/events", tags=["Events"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
