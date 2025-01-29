import uvicorn
from fastapi import FastAPI
from src.reservations.router import router as reservations_router
from src.users.router import router as users_router
from src.events.router import router as events_router
app = FastAPI(
    title="Bookings reservation App"
)

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
