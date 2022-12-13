import csv
import os
import time
# header = ['name','age']
#
# data = [{'name':'suliang','age':'21'},
#         {'name':'xiaoming','age':'22'},
#         {'name':'xiaohu','age':'25'}]
# with open ('information.csv','w',encoding='utf-8',newline='') as fp:
#     # 写
#     writer =csv.DictWriter(fp,header)
#     # 写入标题
#     writer.writeheader()
#     # 将数据写入
#     writer.writerows(data)

topic = "TestUDP"
folder = f"./log/{topic}"

# 判断结果
if not os.path.exists(folder):
    os.makedirs(folder)
    print("OK_folder")

name = topic + "_" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
csvfile = open(f"{folder}/Curve_{name}.csv", "w")
writer = csv.writer(csvfile)
writer.writerow(["frame_num", "Area"])
writer.writerow([1, 2])
