from django.shortcuts import render
import cv2
import imutils
from imutils import contours
import numpy
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
from rest_framework.decorators import api_view

@api_view(['POST'])
def process_image(request):
 

    # img_paths = [
    #     'C://Users//HP//Downloads//try.jpg',
    #     'C://Users//HP//Downloads//try2.jpg'

    # ]
    uploaded_file = request.FILES['image']
    
    file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
    file_path = default_storage.path(file_name)

    first_width = 0

    image = cv2.imread(file_path)
    
    # height, width = image.shape[:2]
    # cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

    # cv2.resizeWindow('Image', width, height)
    # screen_width, screen_height = 1080, 720  

    # Resize the image to fit within the screen resolution   
    # image = cv2.resize(image, (screen_width, screen_height))



    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(11,11),0)


    edged = cv2.Canny(blur,50,100)
    cv2.imshow('canny',edged)
    edged = cv2.dilate(edged,None,iterations=2)
    edged = cv2.erode(edged,None,iterations=1)

    contour = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contour = imutils.grab_contours(contour)

    # cv2.drawContours(image,contour,-1,(0,0,255),4)
    # contour,_ = contours.sort_contours(contour)
    # print(len(contour))

    cont_image = numpy.zeros_like(image)

    max_area = 0
    max_contour = None

    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area>max_area:
            max_area = area
            max_contour = cnt
        
            x,y,w,h = cv2.boundingRect(max_contour)
            

    print("max area  = ",max_area)

    if max_contour is not None:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0,0, 255), 2)
        cv2.putText(image, f'Max Area: {max_area}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # M = cv2.moments(max_contour)
        # centroid_x = int(M['m10'] / M['m00'])
        # centroid_y = int(M['m01'] / M['m00'])
        
        centroid_x = x + w // 2
        centroid_y = y + h // 2 

        image = cv2.circle(image, (centroid_x, centroid_y), 5, (0, 0, 255), -1)
        cv2.drawContours(image, [max_contour], -1, (0, 255, 0), 2)

        # cv2.drawContours(image,contour,-1,(0,255,0),2)
        cv2.imshow('Largest Bounding Rectangle', image)
        print(f"x = {x}, y = {y}, w = {w}, h = {h}")


    
        ellipse_center = (centroid_x, centroid_y)
        axe = (w // 2, h // 2) 
        ellipse_angle = 0
        color = (0, 0, 255)
        cv2.ellipse(image, ellipse_center, axe, ellipse_angle, 0, 360, color, 2)
        cv2.imshow('Largest Bounding Rectangle with Ellipse', image)

    for i, cnt in enumerate(contour):
        cv2.drawContours(cont_image, [cnt], -1, (0, 255, 0), 2)

    cv2.imshow("cont image",cont_image)

    a = w/2
    b = h/2
    w = w*(2.54/96)*0.50
    print("width = ",w)
    h = h*(2.54/96)*0.46
    print("Height = ",h)    
    max_area = max_area*(2.54/96)

    print("area = ",max_area)

    response_data = {
        "message" : "Image Processed Successfully.",  "Height (in cm)" : h ,"Width (in cm)" : w
    }   

    return Response(response_data,status=status.HTTP_200_OK)



    # volume_ell = 1.33*3.14*a*b*first_width
    # volume_ell =  volume_ell*(2.54/96)
    # print("volume of ellipse = ",volume_ell)

    volume = h*w*first_width
    print("volume  = ", volume)


    