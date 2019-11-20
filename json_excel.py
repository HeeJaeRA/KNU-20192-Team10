import os
import pathlib
from openpyxl import Workbook

path_dir = './input'#input폴더에서 json파일 가져옴
file_list = os.listdir(path_dir)
file_list.sort()#파일 이름순으로 정렬

write_wb = Workbook()
write_ws = write_wb.active

count=0
for i in file_list:
    f=open(path_dir+'/'+i)
    keypoint = f.readline()
    keypoint = keypoint[keypoint.find('pose_keypoints_2d":[')+20:keypoint.find('],"face_keypoints_2d"')]
    keypoint = keypoint.split(',')
    count+=1
    for j in range(len(keypoint)):
        write_ws.cell(row=j+1, column = count).value = keypoint[j]

pathlib.Path("./excel_output").mkdir(exist_ok=True)#폴더
write_wb.save('./excel_output/excel_output.xlsx')#저장