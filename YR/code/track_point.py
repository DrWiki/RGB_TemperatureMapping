import cv2
import numpy as np
import os

video_name = '15'
point_cord = [951, 604]
# [951, 604] [970, 620]
memo = list()
flag = True


def draw_rec(x, y, w, h, img):
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 以像素点访问，坐标是（row, col）row < img.rows, col < img.cols
    # 在图像上做画图形，如point（x，y）坐标是（x, y）x < img.cols, y < img.rows

def draw_circle(x, y, img):
    cv2.circle(img, (x, y), 5, (0, 255, 0), 2)


def mouse_callback(event, x, y, flags, param):
    # Check if the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print the coordinates of the mouse click
        print(f'Mouse clicked at (x={x}, y={y})')


def my_filtering(pic):
    # pic = cv2.medianBlur(pic, 5)
    pic = cv2.blur(pic, (9, 9))

    return pic


if __name__ == '__main__':
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    cv2.namedWindow('frame')
    # cv2.namedWindow('ROI', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('frame', mouse_callback)
    vid = cv2.VideoCapture(f'./video/{video_name}.mp4')

    frame_num = 0

    while True:
        ret, frame = vid.read()
        if ret == False:
            break
        if frame_num == 3001:
            break
        # frame = cv2.resize(frame, (640, 480))

        frame_num += 1

        img = frame.copy()
        img = my_filtering(img)  # filtering
        # roi = frame[500:700, 850:1050]
        draw_rec(850, 500, 200, 200, img)
        draw_circle(point_cord[0], point_cord[1], img)
        memo.append(img[point_cord[1], point_cord[0]])
        print(img[point_cord[1], point_cord[0]])

        cv2.imshow('frame', img)
        # cv2.imshow('ROI', roi)
        key = cv2.waitKey(50)

    np.save(f'./data/{point_cord[1]}_{point_cord[0]}_{video_name}.npy', memo)
