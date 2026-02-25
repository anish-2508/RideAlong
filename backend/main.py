from fastapi import FastAPI
from routers.user import router as user_router
from routers.auth import router as auth_router
from routers.ride import router as ride_router
from fastapi import WebSocket, WebSocketDisconnect
from websocket_manager import manager
from services.auth import get_user
from services.auth import decode_token 
from db.database import get_session_local
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#------------------------------------
# this is purely for notifications
#------------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    username = decode_token(token)
    if not username:
        await websocket.close(code=1008)
        return

    SessionLocal = get_session_local()
    db = SessionLocal()

    try:
        user = get_user(db, username)
        if not user:
            await websocket.close(code=1008)
            return
    
        user_id = str(user.userId)
        await manager.connect(user_id, websocket)

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(user_id)

    finally:
        db.close()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(ride_router)



