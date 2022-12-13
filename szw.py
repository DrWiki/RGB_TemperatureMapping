import cv2
import numpy as np
import os

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





if __name__ == '__main__':
    topic = "TestUDP"
    folder = f"./log/{topic}"
    is_need_setting = False
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_origin = cv2.VideoWriter("./video/1.avi", fourcc, 25.0,(int(640), int(480)), True)
    # 判断结果
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("OK_folder")
    # name = topic + "_" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())

    cv2.namedWindow('frame')
    cv2.namedWindow('Plot_frame',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('frame', mouse_callback)
    vid = cv2.VideoCapture('./video/WIN_20221211_13_55_36_Pro.mp4')
    frame_num = 0
    frame_origin = None
    diff = None
    Plot_frame = None
    diff_temp = None
    diff_temp_gray = None

    while True:
        ret, frame = vid.read()
        if ret==False:
            break
        frame = cv2.resize(frame,(640,480) )
        # frame = cv2.medianBlur(frame,9)
        frame = cv2.blur(frame,(19,19))
        img = frame.copy()
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
                cv2.line(Plot_frame,[real_i,255-diff[linep[i][1],linep[i][0],0]],[real_i,255-diff[linep[i+1][1],linep[i+1][0],0]],(255,0,0),1)
                cv2.line(Plot_frame,[real_i,255-diff[linep[i][1],linep[i][0],1]],[real_i,255-diff[linep[i+1][1],linep[i+1][0],1]],(0,255,0),1)
                cv2.line(Plot_frame,[real_i,255-diff[linep[i][1],linep[i][0],2]],[real_i,255-diff[linep[i+1][1],linep[i+1][0],2]],(0,0,255),1)
            for i in range(linep.__len__()):
                cv2.circle(img,[linep[i][0],linep[i][1]],1,(255,255,0),-1)


            diff_temp_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, diff_temp = cv2.threshold(diff_temp_gray, 7, 255, cv2.THRESH_BINARY)
            # diff_temp = cv2.inRange(diff,(7,7,7),(255,255,255))
            # Find the contours in the image
            # continue
            contours, hierarchy = cv2.findContours(diff_temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # # Draw the bounding rectangle of each contour on the original image
            # for contour in contours:
            for i in range(len(contours)):

                x, y, w, h = cv2.boundingRect(contours[i])
                a = cv2.contourArea(contours[i])
                if a < 5000:
                    continue
                print(a)
                cv2.drawContours(diff, contours, i, (0, 0, 255), 3)

                cv2.rectangle(diff, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.putText(img,str(frame_num),(20,20),1,1,(255,255,0),2)


        cv2.imshow("frame", img)
        if Plot_frame is not None:
            cv2.imshow("Plot_frame", Plot_frame)
        if diff is not None:
            cv2.imshow("frame_abs", diff)
        if diff_temp is not None:
            cv2.imshow("diff_temp", diff_temp)
        if diff_temp_gray is not None:
            cv2.imshow("diff_temp_gray", diff_temp_gray)
        out_origin.write(diff)
        key = cv2.waitKey(100)
