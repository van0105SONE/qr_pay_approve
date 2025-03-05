from typing import Union
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import base64
import cv2
import numpy as np
from ultralytics import YOLO
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Define allowed origins (e.g., allow requests from any origin, or specify domains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can specify a list like ["http://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return "You are my special person nah"


@app.websocket("/ws/detect")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Receive base64-encoded frame from the front-end
            data = await websocket.receive_text()
            # Decode the base64 frame
            frame_data = data.split(',')[1]  # Remove the data URL prefix
            frame_bytes = base64.b64decode(frame_data)
            frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

            # Process the frame with YOLO
            detections = await detect_objects(frame)

            await websocket.send_text("")
        except Exception as e:
            print(f"Error: {e}")
            break


async def detect_objects(frame):
    print("it about to procees detection")
    model = YOLO("D:/OPENSOURCE/ocr/delect/best.pt")  # Load YOLO model
    results = model(frame)  # Run YOLO detection
    detected_objects = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Extract (x1, y1, x2, y2)
            print(f"Bounding box: ({x1}, {y1}, {x2}, {y2})")
            class_id = int(box.cls[0])
            object_name = model.names[class_id]
            confidence = float(box.conf[0])
            detected_objects.append({
                'label': object_name,
                'confidence': confidence,
                'box': {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                }
            })
    
    print("detection: ", detected_objects)
    return detected_objects