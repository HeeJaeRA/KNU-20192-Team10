#import Analysis_Data as ad
import Manage_Data as md
import Paint_Graph as pg
import Analysis_Data as ad
import os
import sys

keypoint_name_list = ['Nose', 'Neck', 'RShoulder', 'RElbow', 'RWrist', 'LShoulder', 'LElbow', 'LWrist',
                      'MidHip', 'RHip', 'RKnee', 'RAnkle', 'LHip', 'LKnee', 'LAnkle']
keypoint_num = len(keypoint_name_list)


def main():
    print('현재 경로 >> '+os.getcwd())
    file_path = input("파일 경로 입력 >> ")
    if (os.path.exists(file_path) != True):
        print("Not found " + file_path + "directory!!!")
        sys.exit(0)
    md.merge_JsonFile(file_path)
    s=os.path.split(file_path)
    excel_saveName = s[len(s)-1]+'.xlsx'
    all_value = md.get_data(file_path+'/'+excel_saveName)
    all_x_keypoint, all_y_keypoint = md.refine_data(all_value, file_path+'/'+excel_saveName)
    ad.analysis(all_x_keypoint, all_y_keypoint)
    pg.Paint_Graph(ad.input_x_keypoint, ad.input_y_keypoint)
    pg.Paint_Graph(all_x_keypoint, all_y_keypoint)

if __name__ == '__main__':
  main()


