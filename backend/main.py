from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
from sre_parse import State
import numpy as np
from matplotlib import pyplot as plt
import imutils
import easyocr
import cv2
from stateName import *
from String_m import *
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# uvicorn main:app --reload --host 0.0.0.0 --port 8000

app = FastAPI()

origins = [
    "http://localhost:3000",       
    "http://frontend:3000"    # When containers talk to each other via service name   # Optional if you access via IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow your frontend
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, etc.
    allow_headers=["*"],    # allow all headers
)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read uploaded bytes directly (no local save)
        contents = await file.read()
        # Convert bytes data to numpy array then decode to image
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return JSONResponse({"error": "Could not decode image"}, status_code=400)

        # Process image in-memory
        result = my_image_processing(img)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

def my_image_processing(img):
    """Process an image (numpy array BGR) and return detected text.
    img: numpy.ndarray in BGR color space (as returned by cv2.imdecode)
    """
    res_text=[0]
    res_img=[0]
    # img is expected to be a numpy array (BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(gray, (3,3), 0) 
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) 
    
    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) 
    contours, hierarchy = cv2.findContours(image=edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    image_copy = img.copy()
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    contours= sorted(contours, key=cv2.contourArea, reverse= True)[:30]
    location = None
    screenCnt = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            screenCnt = approx
            x,y,w,h = cv2.boundingRect(contour) 
            new_img=img[y:y+h,x:x+w]
            break
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask,  [screenCnt],0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    try:
        text = result[0][1]
    except IndexError:
        result = reader.readtext(img)
        text=result[0][1]

    text=Random(text)
    text=change(text)
    text=space(text)
    text=Manipulate(text)
    print(text)
    #STATES 
    s=stateName(text)
    print(s)
    return {"plate":text,"state":s}
