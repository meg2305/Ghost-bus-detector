from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "WebSocket test server is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("✅ WebSocket connection established!")

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print("❌ WebSocket disconnected:", e)

@app.on_event("startup")
async def list_routes():
    print("Registered routes:")
    for route in app.routes:
        if hasattr(route, "methods"):  # HTTP routes
            print(route.path, route.methods)
        else:  # WebSocket routes
            print(route.path, "WebSocket")


if __name__ == "__main__":
    uvicorn.run("ws_test:app", host="127.0.0.1", port=8000, reload=True)
