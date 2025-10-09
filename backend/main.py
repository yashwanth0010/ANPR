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

app = FastAPI()

origins = [
    "http://localhost:3000",       # React dev server
    "http://172.29.78.177:8000"    # Optional if you access via IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow your frontend
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, etc.
    allow_headers=["*"],    # allow all headers
)

app = FastAPI()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Save the uploaded file
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Run your image processing script here
    result = my_image_processing(file_location)  # define your function
    
    return JSONResponse({"result": result})

def my_image_processing(path):
    res_text=[0]
    res_img=[0]
    img = cv2.imread(path)
   # img=img.resize((300,300))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
    #plt.show()

    img_blur = cv2.GaussianBlur(gray, (3,3), 0) 
    #plt.imshow(img_blur, cmap = 'gray', interpolation = 'bicubic')
    #plt.show()

    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) 

    """plt.imshow(sobelx, cmap = 'gray', interpolation = 'bicubic')
    plt.show()
    plt.imshow(sobely, cmap = 'gray', interpolation = 'bicubic')
    plt.show()
    plt.imshow(sobelxy, cmap = 'gray', interpolation = 'bicubic')
    plt.show()"""
    
    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) 
   # plt.imshow(edges, cmap = 'gray', interpolation = 'bicubic')
    #plt.show()

    contours, hierarchy = cv2.findContours(image=edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    image_copy = img.copy()
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    #plt.imshow(image_copy, cmap = 'gray', interpolation = 'bicubic')
    #plt.show()



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
            #cv2.imwrite('./'+str(i)+'.png',new_img)
            #i+=1
            break

    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
    #plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    #plt.show()

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask,  [screenCnt],0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    ##plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

    #plt.imshow(new_image, cmap = 'gray', interpolation = 'bicubic')
    #plt.show()

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    #plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

    #plt.imshow(cropped_image, cmap = 'gray', interpolation = 'bicubic')
    #plt.show()

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
    

    print(type(text))
    print(text)

    #STATES 
    s=stateName(text)
    print(s)
    #res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    #res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[0][0]), (0,255,0),3)

    """plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    #uploaded=Image.open("result.png")
    """im=ImageTk.PhotoImage(uploaded)
    plate_image.configure(image=im)
    plate_image.image=im
    plate_image.pack()
    plate_image.place(x=560,y=320)"""
    return text
