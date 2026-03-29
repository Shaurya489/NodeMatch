from fastapi import FastAPI, WebSocket

waiting_pool=[]
active_chats={}

app=FastAPI()

@app.get("/")


@app.websocket("/ws")

async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    if waiting_pool:
        partner=waiting_pool.pop(0)
        active_chats[websocket]=partner
        active_chats[partner]=websocket
        
        await websocket.send_text("Connected to a stranger")
        await partner.send_text("Connected to a stranger")
    else:
        waiting_pool.append(websocket)
        await websocket.send_text("Searching for people...")
    
    try:
        while True:
            message=await websocket.receive_text()
            
            partner=active_chats.get(websocket)
            
            if partner:
                await partner.send_text(message)
    except WebSocketDisconnect:
        if websocket in waiting_pool:
            waiting_pool.remove(websocket)
        partner=active_chats.get(websocket)
        if partner:
            await partner.send_text("Stranger has disconnected.")
            del active_chats[partner]
            del active_chats[websocket]