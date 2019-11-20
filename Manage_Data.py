import os
import sys
from openpyxl import load_workbook, Workbook
import Main

remove_keypoint_num = 10 #눈,귀,발 제외(15~24)
Runge_CompData_path = './Data/Runge_CompData.xlsx'
Squat_CompData_path = './Data/Squat_CompData.xlsx'

def merge_JsonFile(dir_path):
    if (os.path.exists(dir_path)!=True):
        print("Not found "+dir_path+" directory!!!")
        sys.exit(0)
    file_list = os.listdir(dir_path)
    file_list.sort()

    write_wb = Workbook()
    write_ws = write_wb.active

    os.chdir(dir_path)

    count = 0;
    for i in file_list  :
        fname, ext = os.path.splitext(i)
        if(ext=='.json'):
            count+=1
            f= open(i)
            keypoint = f.readline()
            keypoint = keypoint[keypoint.find('pose_keypoints_2d":[') + 20:keypoint.find('],"face_keypoints_2d"')]
            keypoint = keypoint.split(',')
            for j in range(len(keypoint)):
                keypoint[j]=float(keypoint[j])
                write_ws.cell(row=j+1, column = count).value = keypoint[j]

    dir_name = dir_path.split(os.path.sep)
    dir_name = dir_name[len(dir_name)-1]
    save_name = dir_name +'.xlsx'
    write_wb.save(save_name)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))#현재 디렉토리를 원래 경로로 바꿈


def get_data(file_path, m=0):#i==0:input data, #i==1:comparisonData
    if (os.path.exists(file_path) != True):
        print("Not found '" + file_path + "!!!")
        return -1

    load_wb = load_workbook(file_path, data_only=True)
    load_ws = load_wb['Sheet']

    i = 0
    all_x_values = []
    all_y_values = []

    if(m==1):
        for row in load_ws.rows:
            keypoint_value = []
            for cell in row:
                if(float(cell.value)<0):
                    continue
                keypoint_value.append(float(cell.value))
            if(i%2==0):
                all_x_values.append(keypoint_value)
            elif(i%2==1):
                all_y_values.append(keypoint_value)
            i=i+1
        return all_x_values, all_y_values

    else:
        all_c_values = []
        for row in load_ws.rows:
            keypoint_value = []
            for cell in row:
                if(float(cell.value)<0):
                    continue
                keypoint_value.append(float(cell.value))
            if(i%3==0):
                all_x_values.append(keypoint_value)
            elif(i%3==1):
                all_y_values.append(keypoint_value)
            else:#i%3==2
                all_c_values.append(keypoint_value)
            i=i+1
        all_values = []
        all_values.append(all_x_values)
        all_values.append(all_y_values)
        all_values.append(all_c_values)
        return all_values


def refine_data(_3d_list, save_path):
    write_wb = Workbook()
    write_ws = write_wb.active

    all_x_keypoint = []
    all_y_keypoint = []

    for i in range((len(_3d_list[0]))-remove_keypoint_num):#_3d_list[0]:x, [1]:y, [2]:c
        keypoint_x = []
        keypoint_y = []
        for j in range(len(_3d_list[0][i])):
            if (_3d_list[2][i][j] >= 0.2):
                keypoint_x.append(_3d_list[0][i][j])
                keypoint_y.append(_3d_list[1][i][j])
                write_ws.cell(row=(i*2)+1, column = j+1).value = _3d_list[0][i][j]
                write_ws.cell(row=(i+1)*2, column = j+1).value = _3d_list[1][i][j]
            else:
                #keypoint_x.append(-1)
                #keypoint_y.append(-1)
                write_ws.cell(row=(i*2)+1, column=j+1).value = -1
                write_ws.cell(row=(i+1)*2, column=j+1).value = -1
        all_x_keypoint.append(keypoint_x)
        all_y_keypoint.append(keypoint_y)

    write_wb.save(save_path)

    return all_x_keypoint, all_y_keypoint