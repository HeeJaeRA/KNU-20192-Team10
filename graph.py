import matplotlib.pyplot as plt
from openpyxl import load_workbook

keypoint_name_list = ['Nose', 'Neck', 'RShoulder', 'RElbow', 'RWrist', 'LShoulder', 'LElbow', 'LWrist',
                      'MidHip', 'RHip', 'RKnee', 'RAnkle', 'LHip', 'LKnee', 'LAnkle', 'REye', 'LEye', 'REar', 'LEar',
                      'LBigToe', 'LSmallToe', 'LHeel', 'RBigToe', 'RSmallToe', 'RHeel']

load_wb = load_workbook('./excel_output/excel_output.xlsx', data_only=True)#엑셀파일 위치
load_ws=load_wb['Sheet']

all_values = []
for row in load_ws.rows:
    keypoint_value=[]
    for cell in row:
        keypoint_value.append(float(cell.value))
    all_values.append(keypoint_value) #일단 엑셀파일 다 읽어옴

#그래프 x,y한번에 그리기
for i in range(len(keypoint_name_list)):
    plt.plot(all_values[i*2], label=keypoint_name_list[i]+'_x')
    plt.legend()
plt.show()
for i in range(len(keypoint_name_list)):
    plt.plot(all_values[i * 2 + 1], label=keypoint_name_list[i]+'_y')
    plt.legend()
plt.show()

'''
#그래프 x,y한개씩 따로 그리기
for i in range(len(keypoint_name_list)):
    plt.plot(all_values[i*2], label=keypoint_name_list[i]+'_x')
    plt.legend()
    plt.show()
    plt.plot(all_values[i*2+1], label=keypoint_name_list[i]+'_y')
    plt.legend()
    plt.show()
'''
