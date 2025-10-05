from sre_parse import State
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from tkinter import PhotoImage
import numpy as np
from matplotlib import pyplot as plt
import imutils
import easyocr
import cv2
import pytesseract as tess
from stateName import *
from String_m import *
import openpyxl 
from datetime import datetime

now = datetime.now()

wb = openpyxl.load_workbook("Data.xlsx") 
  
sheet = wb.active


top=tk.Tk()
top.geometry('1920x1080')
top.title('Number Plate Recognition')
#top.iconphoto(True, PhotoImage(file="logo.jpg"))

top.iconphoto(True, PhotoImage(file="logo_w.png"))
img = ImageTk.PhotoImage(Image.open("logo_w.png"))

label = Label(top, text = "ANPR",bg="#353935",fg="#0313fc",font=('Times', 35))
label.pack()

im1=Image.open("logo_w.png")
ima = im1.resize((330,260))
img = ImageTk.PhotoImage(ima)

top.configure(background='#353935')
label=Label(top,background='#CDCDCD', font=('arial',35,'bold'))

label1 = tk.Label(image=img)
label1.image = ima
label1.place(x=600, y=70)

label.pack()

#label.grid(row=0,column=1)
ran=Image.open("Upload2.jpg")
ran=ran.resize((300,200))
up=ImageTk.PhotoImage(ran)

sign_image = Label(top,image=up)  
plate_image=Label(top,bd=10)

State1 = Label(top, text = "",bg="#353935",foreground='#FFFFFF', font=('Times', 24))


def classify(file_path):
    res_text=[0]
    res_img=[0]
    img = cv2.imread(file_path)
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

    #DATA INTO EXCEL SHEET
    now = datetime.now()
    dt= now.strftime("%d/%m/%Y %H:%M:%S")
    data=(dt[0:11],dt[11:len(dt)],text,s[8:len(s)])
    print(dt)
    sheet.append(data)
    wb.save('Data.xlsx')

    font = cv2.FONT_HERSHEY_SIMPLEX
    #res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    #res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[0][0]), (0,255,0),3)

    """plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    label.configure(foreground='#FFFFFF', text=text,bg="#353935") 

    State1.configure(text=s)

    #uploaded=Image.open("result.png")
    """im=ImageTk.PhotoImage(uploaded)
    plate_image.configure(image=im)
    plate_image.image=im
    plate_image.pack()
    plate_image.place(x=560,y=320)"""

def show_classify_button(file_path):
    classify_b=Button(top,text="Get Text",command=lambda: classify(file_path),padx=10,pady=5)
    classify_b.configure(background='#3734eb', foreground='white',font=('arial',15,'bold'))
    classify_b.place(x=1000,y=650)

def upload_image():
    try:
        file_path=filedialog.askopenfilename()
        uploaded=Image.open(file_path)
        
        uploaded.thumbnail(((top.winfo_width()/5),(top.winfo_height()/5)))
        #uploaded.place(x=650, y=2000)
        

        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        #sign_image=sign_image.resize((300,300))
        #sign_image.place(x=100, y=400)     
        label.configure(text='')

        State1.configure(text='')
        show_classify_button(file_path)
    except:
        pass

upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
upload.configure(background='#3734eb', foreground='white',font=('arial',15,'bold'))
upload.pack()
upload.place(x=210,y=650)

sign_image.pack()
sign_image.place(x=150,y=400)

label.pack()
label.place(x=925,y=400)

State1.pack()
State1.place(x = 925,y =500 )


#heading = Label(top,image=None)
#heading.configure(background='#3734eb',foreground='#3734eb')
#heading.pack()

top.mainloop()