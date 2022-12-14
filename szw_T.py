import cv2
import numpy as np
import os
import csv
import time
points = list()
linep = list()
# img = np.zeros([1000, 1000])
img = cv2.imread("./1.jpg")
# 通用的Bresenham算法
def GenericBresenhamLine(img, p0, p1, color):
    x1, y1, x2, y2 = p0[0],p0[1],p1[0],p1[1]
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    # 根据直线的走势方向，设置变化的单位是正是负
    s1 = 1 if ((x2 - x1) > 0) else -1
    s2 = 1 if ((y2 - y1) > 0) else -1
    # 根据斜率的大小，交换dx和dy，可以理解为变化x轴和y轴使得斜率的绝对值为[0,1]
    boolInterChange = False
    if dy > dx:
        np.swapaxes(dx, dy)
        boolInterChange = True
    # 初始误差
    e = 2 * dy - dx
    x = x1
    y = y1
    count = 0
    tem_c = 0
    for i in range(0, int(dx + 1)):
        cv2.circle(img,[x,y],1,color,-1)
        linep.append([x,y])
        if count % 100 ==0:
            cv2.putText(img,str(tem_c),[x,y],1,1,(255,0,0),1)
            tem_c = tem_c + 1
        count = count + 1
        if e >= 0:
            # 此时要选择横纵坐标都不同的点，根据斜率的不同，让变化小的一边变化一个单位
            if boolInterChange:
                x += s1
            else:
                y += s2
            e -= 2 * dx
        # 根据斜率的不同，让变化大的方向改变一单位，保证两边的变化小于等于1单位，让直线更加均匀
        if boolInterChange:
            y += s2
        else:
            x += s1
        e += 2 * dy


def mouse_callback(event, x, y, flags, param):
    # Check if the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print the coordinates of the mouse click
        if points.__len__() < 2:
            points.append([x, y])
            print(f'Mouse clicked at (x={x}, y={y})')

    if event == cv2.EVENT_MBUTTONDOWN:
        # Print the coordinates of the mouse click
        if points.__len__() == 2:
            GenericBresenhamLine(img,points[0],points[1],(255,0,0))
        cv2.imshow('frame', img)
        print(linep)


def d_image_xy(II, flag = 'x'):
    g = np.zeros(II.shape,dtype=np.float64)
    # I.dtype= np.dtype("float64")
    I = II.astype('float64')
    if flag=='x':
        g[:,:-1] = I[:,1:]-I[:,:-1]
    elif flag=='y':
        g[:-1,:] = I[1:, :] - I[:-1,:]
    else :
        g=I
    return g


def cvtRGBT(I, w0, w1, w2):
    I = I.astype('float')
    return (w0*I[:, :, 0]+w1*I[:, :, 1]+w2*I[:, :, 2])/3


if __name__ == '__main__':
    topic = "TestUDP"
    folder = f"./log/{topic}"

    # 判断结果
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("OK_folder")

    name = topic + "_" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
    csvfile = open(f"{folder}/Curve_{name}.csv", "w",encoding='utf8',newline='')
    writer = csv.writer(csvfile)
    writer.writerow(["frame_num", "Area"])
    is_need_setting = False
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_origin = cv2.VideoWriter("./video/1.avi", fourcc, 25.0,(int(640), int(480)), True)

    # name = topic + "_" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())

    cv2.namedWindow('frame')
    cv2.namedWindow('Plot_frame',cv2.WINDOW_NORMAL)

    # cv2.setMouseCallback('frame', mouse_callback)

    vid = cv2.VideoCapture('./video/WIN_20221211_13_55_36_Pro.mp4')

    frame_num = 0
    frame_origin = None
    diff = None
    Plot_frame = None
    diff_temp = None
    diff_temp_gray = None
    laplace_x = None
    laplace_my = None
    frame_gray = None
    mask = None
    diff_mask = None
    diff_mask_gray = None
    diff_mask_gray_cv = None
    last_frame = []
    kpc = None


    while True:
        ret, frame = vid.read()
        if ret==False:
            break
        frame = cv2.resize(frame,(640,480) )
        frame = cv2.blur(frame,(33,33))
        img = frame.copy()
        img_pro = frame.copy()
        cv2.imshow("frame", img)
        frame_num = frame_num + 1
        if frame_num <90:
            continue
        if frame_num < 100:
            frame_origin = frame.copy()
            if is_need_setting:
                key = cv2.waitKey(0)
                if key == ord('s'):
                    np.save('linep.npy', points+linep)
                    lomy_list = np.load('linep.npy')
                    points = [lomy_list[0]]
                    linep = lomy_list[1:]
                    print(lomy_list)
            else:
                lomy_list = np.load('linep.npy')
                points = [lomy_list[0]]
                linep = lomy_list[1:]
                print(lomy_list)
        else:
            diff = cv2.absdiff(frame, frame_origin)

        if diff is not None:
            Plot_frame = np.zeros((300, linep.__len__()*2, 3), dtype=np.int8)

            for i in range(linep.__len__()-1):
                real_i = i*2
                # cv2.circle(Plot_frame,[i,img[linep[i][1],linep[i][0],2]],2,(255,0,0),-1)
                cv2.line(Plot_frame, [real_i,255-diff[linep[i][1],linep[i][0],0]],
                         [real_i,255-diff[linep[i+1][1],linep[i+1][0],0]],(255,0,0),1)
                cv2.line(Plot_frame, [real_i,255-diff[linep[i][1],linep[i][0],1]],
                         [real_i,255-diff[linep[i+1][1],linep[i+1][0],1]],(0,255,0),1)
                cv2.line(Plot_frame, [real_i,255-diff[linep[i][1],linep[i][0],2]],
                         [real_i,255-diff[linep[i+1][1],linep[i+1][0],2]],(0,0,255),1)

                Temp_t0 = 255-int((diff[linep[i][1], linep[i][0], 0]+diff[linep[i][1], linep[i][0], 1]-0*diff[linep[i][1], linep[i][0], 2]))
                Temp_t1 = 255-int((diff[linep[i+1][1], linep[i+1][0], 0]+diff[linep[i+1][1], linep[i+1][0], 1]-0*diff[linep[i+1][1], linep[i+1][0], 2]))
                cv2.line(Plot_frame, [real_i, Temp_t0],
                         [real_i, Temp_t1], (255, 0, 255), 1)
            for i in range(linep.__len__()):
                cv2.circle(img,[linep[i][0],linep[i][1]],1,(255,255,0),-1)

            diff_temp_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, diff_temp = cv2.threshold(diff_temp_gray, 10, 255, cv2.THRESH_BINARY)
            # diff_temp = cv2.inRange(diff,(7,7,7),(255,255,255))
            # Find the contours in the image
            # continue
            contours, hierarchy = cv2.findContours(diff_temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # # Draw the bounding rectangle of each contour on the original image
            # for contour in contours:
            maxA = 0
            maxAid = -1
            for i in range(len(contours)):
                a = cv2.contourArea(contours[i])
                if a < 5000:
                    continue
                if a > maxA:
                    maxA = a
                    maxAid = i
            if maxAid>=0:
                # print(maxA)
                mask = np.zeros(diff_temp_gray.shape, dtype='uint8')
                cv2.drawContours(mask, contours, maxAid, 255, -1)
                diff_mask = cv2.bitwise_and(img_pro, img_pro, mask=mask)
                diff_mask_gray = cvtRGBT(diff_mask,1,1,-1).astype('uint8')
                laplace_x = cv2.Laplacian(diff_mask_gray, cv2.CV_64F)
                # print(laplace_x.dtype)
                # laplace_x = laplace_x.astype('uint8')
                # kernal = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
                # laplace_x = cv2.dilate(laplace_x,kernal)
                # laplace_x = cv2.erode(laplace_x,kernal)
                cv2.drawContours(diff, contours, maxAid, (0, 0, 255), 3)
                x, y, w, h = cv2.boundingRect(contours[maxAid])
                cv2.rectangle(diff, (x, y), (x + w, y + h), (255, 0, 0), 2)
                writer.writerows([[frame_num, maxA]])

        Time_int = 10
        if last_frame.__len__()<Time_int:
            last_frame.append(frame.copy())
        else:
            last_frame.pop(0)
            last_frame.append(frame.copy())

        cv2.putText(img,str(frame_num),(20,20),1,1,(255,255,0),2)
        cv2.imshow("frame", img)


        if frame_gray is not None:
            cv2.imshow("frame_gray", frame_gray)
        if Plot_frame is not None:
            cv2.imshow("Plot_frame", Plot_frame)
        if diff is not None:
            cv2.imshow("frame_abs", diff)
        if diff_temp is not None and False:

            cv2.imshow("diff_temp", diff_temp)
        if diff_temp_gray is not None and False:
            cv2.imshow("diff_temp_gray", diff_temp_gray)

        if laplace_x is not None:
            cv2.imshow("laplace_x", laplace_x)
        if laplace_my is not None:
            cv2.imshow("laplace_my", laplace_my)
        if diff_mask is not None and False:
            cv2.imshow("diff_mask", diff_mask)
        if diff_mask_gray is not None:
            cv2.imshow("diff_mask_gray", diff_mask_gray)
        if diff_mask_gray_cv is not None:
            cv2.imshow("diff_mask_gray_cv", diff_mask_gray_cv)

        if diff_mask_gray_cv is not None and diff_mask_gray is not None:
            print(diff_mask_gray.dtype)
            print(diff_mask_gray_cv.dtype)
            cv2.imshow("diff_mask_gray_cv", cv2.absdiff(diff_mask_gray,diff_mask_gray_cv))

        # if last_frame is not None:
        #     cv2.imshow("last_frame", cv2.absdiff(last_frame,frame))
        if last_frame.__len__()==Time_int and laplace_x is not None:
            cv2.imshow("last_frame", cv2.absdiff(last_frame[0], frame)*5)
            kpc = (cvtRGBT((frame.astype('float')-last_frame[0].astype('float')),1,1,-1)/(laplace_x+0.001))/100000
            cv2.imshow("KKKKKKK", kpc)
            print("Kpc:   ",np.sum(np.sum(kpc,0),0))

        out_origin.write(diff)
        key = cv2.waitKey(10)
