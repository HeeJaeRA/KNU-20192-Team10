import numpy as np
import DTW
import Manage_Data as md
import Main
import operator
import Paint_Graph as pg

input_x_keypoint = []
input_y_keypoint = []
frame_limit = 50
squ_corrcoef = []
len_corrcoef = []
flk_corrcoef = []
squ_weight = [[0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0, 3, 3, 0.5, 1.5, 3, 0.5, 1.5],[0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0, 3, 3, 0.5, 1.5, 3, 0.5, 1.5]]
lun_weight = [[0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0, 1.5, 1.5, 2, 2, 2, 2, 2],[0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0, 3, 3, 0.5, 1.5, 3, 0.5, 1.5]]
flk_weight = [[0, 1, 1, 0, 0, 1, 0, 0, 2, 2, 1.5, 1.5, 2, 1.5, 1.5],[0, 1, 1, 0, 0, 1, 0, 0, 2, 2, 1.5, 1.5, 2, 1.5, 1.5]]

def reduce_frame(keypoint_list):
    reduced_list = []
    n = len(keypoint_list)
    if(n<=frame_limit):
        return keypoint_list
    partition_size = round((2*n/(frame_limit+2)),0)
    i=0
    while(1):
        if(i+partition_size >=n):
            avg = sum(keypoint_list[i:n])/len(keypoint_list[i:n])
            reduced_list.append(avg)
            break
        start_index = i
        end_index = int(i + partition_size)
        avg = sum(keypoint_list[start_index:end_index])/len(keypoint_list[start_index:end_index])
        reduced_list.append(avg)
        i=i+int(partition_size/2)
    return reduced_list


def comparison_Data(keypoint, weight_list):
    #squat_x_keypoint, squat_y_keypoint = md.get_data(md.Squat_CompData_path, 1)
    for i in range(len(keypoint[0])):
        keypoint[0][i] = reduce_frame(keypoint[0][i])
    for i in range(len(keypoint[1])):
        keypoint[1][i] = reduce_frame(keypoint[1][i])

    for j in range(9,12):
        if(np.std(keypoint[0][j])<np.std(keypoint[0][j+3])):
            keypoint[0][j], keypoint[0][j+3] = keypoint[0][j+3], keypoint[0][j]
        if(np.std(input_x_keypoint[j])<np.std(input_x_keypoint[j+3])):
            input_x_keypoint[j], input_x_keypoint[j+3] = input_x_keypoint[j+3], input_x_keypoint[j]
        if (np.std(keypoint[1][j]) < np.std(keypoint[1][j + 3])):
            keypoint[1][j], keypoint[1][j + 3] = keypoint[1][j + 3], keypoint[1][j]
        if (np.std(input_y_keypoint[j]) < np.std(input_y_keypoint[j + 3])):
            input_y_keypoint[j], input_y_keypoint[j + 3] = input_y_keypoint[j + 3], input_y_keypoint[j]

    #pg.Paint_Graph_DTW(input_x_keypoint, input_y_keypoint, keypoint[0], keypoint[1])


    result = 0
    for i in range(len(input_x_keypoint)):
        if(len(input_x_keypoint[i])==0):
            continue
        if(weight_list[0][i]!=0):
            coef = DTW.DTW(input_x_keypoint[i], keypoint[0][i], " : "+Main.keypoint_name_list[i]+"_x")
            #print(abs(coef))
            coef = coef*weight_list[0][i]
            result += abs(coef)

    if (keypoint[1][1][int(len(keypoint[1][1]) / 2)] > keypoint[1][14][int(len(keypoint[1][14]) / 2)]):
        for i in range(len(input_y_keypoint)):
            if (len(input_y_keypoint[i]) == 0):
                continue
            if (weight_list[1][i] != 0):
                coef = DTW.DTW(input_y_keypoint[i], keypoint[1][i], " : " + Main.keypoint_name_list[i] + "_y")
                #print(abs(coef))
                coef = coef * weight_list[1][i]
                result += abs(coef)
    else:
        for i in range(len(input_y_keypoint)):
            if(len(input_y_keypoint[i])==0):
                continue
            if(weight_list[1][i]!=0):
                coef = DTW.DTW(input_y_keypoint[i], keypoint[1][i], " : "+Main.keypoint_name_list[i]+"_y")
                #print(coef)
                coef = coef*weight_list[1][i]
                result += coef

    #print("Total coef : "+str(result))
    return result


def analysis(all_x_keypoint, all_y_keypoint):
    global input_x_keypoint
    global input_y_keypoint
    input_x_keypoint = list(all_x_keypoint)
    input_y_keypoint = list(all_y_keypoint)

    for i in range(len(input_x_keypoint)):
        input_x_keypoint[i] = reduce_frame(input_x_keypoint[i])
    for i in range(len(input_y_keypoint)):
        input_y_keypoint[i] = reduce_frame(input_y_keypoint[i])

    #md.save_reduceList_toExcel(input_x_keypoint, input_y_keypoint)

    Squat_coef = comparison_Data(md.get_data(md.Squat_CompData_path, 1), squ_weight)
    Lunge_coef = comparison_Data(md.get_data(md.Lunge_CompData_path, 1), lun_weight)
    Flank_coef = comparison_Data(md.get_data(md.Flank_CompData_path, 1), flk_weight)
    #max_coef = max(Squat_coef, Lunge_coef, Flank_coef)
    max_coef = [('Squat', Squat_coef), ('Lunge',Lunge_coef), ('Flank', Flank_coef)]
    max_coef = sorted(max_coef, key=operator.itemgetter(1), reverse=True)

    for i in range(len(max_coef)):
        print(str(i+1)+'.', end=" ")
        print(max_coef[i][0], end=" ")
        print('('+str(max_coef[i][1]/30*100)+'%)')

    if(max_coef[0][1]==Squat_coef):
        print('운동명칭: 스쿼트')
        print('운동정보 : https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/135/bodyweight-squat')
    elif(max_coef[0][1]==Lunge_coef):
        print('운동명칭 : 런지')
        print('운동정보 : https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/137/standing-lunge-stretch')
    elif(max_coef[0][1]==Flank_coef):
        print('운동명칭 : 플랭크')
        print('운동정보 : https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/32/front-plank')

