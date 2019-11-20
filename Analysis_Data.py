import DTW
import Manage_Data as md
import Main

input_x_keypoint = []
input_y_keypoint = []
frame_limit = 50
squ_corrcoef = []
len_corrcoef = []
push_corrcoef = []

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

def comparison_Squat():
    squat_x_keypoint, squat_y_keypoint = md.get_data(md.Squat_CompData_path, 1)
    for i in range(len(squat_x_keypoint)):
        squat_x_keypoint[i] = reduce_frame(squat_x_keypoint[i], )
    for i in range(len(squat_y_keypoint)):
        squat_y_keypoint[i] = reduce_frame(squat_y_keypoint[i])

    result = 0
    for i in range(len(input_x_keypoint)):
        if(len(input_x_keypoint[i])==0):
            continue
        result += DTW.DTW(input_x_keypoint[i], squat_x_keypoint[i], "Squat : "+Main.keypoint_name_list[i]+"_x")
        #print("vs. Squat "+Main.keypoint_name_list[i]+'_x : ' + str(coef))
    for i in range(len(input_y_keypoint)):
        if(len(input_y_keypoint[i])==0):
            continue
        result += DTW.DTW(input_y_keypoint[i], squat_y_keypoint[i], "Squat : "+Main.keypoint_name_list[i]+"_y")
    print("total coef : "+str(result))
    return result

def comparison_Runge():
    runge_x_keypoint, runge_y_keypoint = md.get_data(md.Runge_CompData_path, 1)
    for i in range(len(runge_x_keypoint)):
        runge_x_keypoint[i] = reduce_frame(runge_x_keypoint[i], )
    for i in range(len(runge_y_keypoint)):
        runge_y_keypoint[i] = reduce_frame(runge_y_keypoint[i])
    coef = 0
    for i in range(len(input_x_keypoint)):
        if(len(input_x_keypoint[i])==0):
            continue
        coef += DTW.DTW(input_x_keypoint[i], runge_x_keypoint[i], "Runge : "+Main.keypoint_name_list[i]+"_x")
    for i in range(len(input_y_keypoint)):
        if(len(input_y_keypoint[i])==0):
            continue
        coef += DTW.DTW(input_y_keypoint[i], runge_y_keypoint[i], "Runge : "+Main.keypoint_name_list[i]+"_y")
    print("total coef : "+str(coef))
    return coef


def analysis(all_x_keypoint, all_y_keypoint):
    global input_x_keypoint
    global input_y_keypoint
    input_x_keypoint = list(all_x_keypoint)
    input_y_keypoint = list(all_y_keypoint)

    for i in range(len(input_x_keypoint)):
        input_x_keypoint[i] = reduce_frame(input_x_keypoint[i])
    for i in range(len(input_y_keypoint)):
        input_y_keypoint[i] = reduce_frame(input_y_keypoint[i])

    Squat_coef = comparison_Squat()
    Runge_coef = comparison_Runge()
    if(Squat_coef > Runge_coef):
        print("Squat")
    elif(Runge_coef > Squat_coef):
        print("Runge")
    else:
        print("Squat/Runge")