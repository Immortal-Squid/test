import cv2
import numpy as np
import math

def darker(img):
    """降低亮度，辅助函数"""
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 转换为 HSV 颜色空间
    hsv_image[:, :, 2] = hsv_image[:, :, 2] * 0.5  # 将 V 通道乘以 0.5
    darker_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)  # 转换回 BGR
    return darker_image

def process_img(img, val):
    """处理图像，返回二值图像、调整大小和亮度的图像"""    
    img_resized = cv2.resize(img, (640, 480))  # 调整图像大小
    img_dark = cv2.convertScaleAbs(img_resized, alpha=0.5)  # 调整亮度
    img_darker = darker(img_dark)  # 降低亮度
    img_gray = cv2.cvtColor(img_darker, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    _, img_binary = cv2.threshold(img_gray, val, 255, cv2.THRESH_BINARY)  # 二值化处理
    cv2.imshow("Binary Image", img_binary)  # 显示二值图像
    return img_dark, img_binary 

def adjust(rect):
    c,(w,h),angle=rect
    if w>h:
        angle=(angle+90)%360
        angle=angle-360 if angle>180 else angle -180 if angle>90 else angle
    return c,(w,h),angle

def find_light(resized_img,binary_img):
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects=[]
    for countour in contours:
        rect=cv2.minAreaRect(countour)
        area=cv2.contourArea(countour)
        if area<5:
            continue
        rect=adjust(rect)
        if -35<rect[2]<35:
            box=cv2.boxPoints(rect)
            box=np.int0(box)
            rects.append(rect)
            cv2.drawCountours(resized_img,[box],0,(0,255,0),2)
            return resized_img,rects
        
        def is_close(rect1,rect2,light_angle_tol,line_angle_tol,height_tol,cy_tol):
            
