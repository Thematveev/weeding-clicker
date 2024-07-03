from fastapi import FastAPI, WebSocket, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect


import models
from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


templates = Jinja2Templates(directory='templates')

@app.get('/')
def main(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@app.websocket('/ws')
async def websock_endpoint(websocket: WebSocket, db: Session=Depends(get_db)):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            print(data)
        except WebSocketDisconnect:
            break
        

        user = db.query(models.User).filter(models.User.userId == data['id']).first()

        if data['type'] == 'auth':
            
            if not user:
                user = models.User(
                    username=data['username'],
                    userId=data['id'],
                    score=0
                )
                db.add(user)
                db.commit()

            
            await websocket.send_json({
                'type': 'info',
                'score': user.score
            })

        elif data['type'] == 'increase':
            user.score = data['value']
            db.add(user)
            db.commit()
        
            