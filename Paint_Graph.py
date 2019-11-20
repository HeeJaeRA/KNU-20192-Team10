import matplotlib.pyplot as plt
import Main

def Paint_CostMatrix(acc_cost_matrix, path, label=" "):
    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w', label=label)
    plt.legend()
    plt.show()

def Paint_ComparisonGraph(keypoint1, keypoint2, keypoint1_dtw, label=" "):
    plt.figure(figsize=(15, 8))
    plt.subplot(1,2,1)
    plt.title('Comparison : input '+label +' vs. Standard ' +label)
    plt.plot(keypoint1)
    plt.plot(keypoint2)
    plt.legend([label, 'Standard '+label])
    plt.grid(True)
    plt.ylim((0, 1920))
    plt.subplot(1,2,2)
    plt.title('Comparison : input '+label +'_dtw vs. Standard ' +label)
    plt.plot(keypoint1_dtw)
    plt.plot(keypoint2)
    plt.legend([label+'_dtw', 'Standard '+label])
    plt.grid(True)
    plt.ylim((0, 1920))
    plt.show()

def Paint_Graph_DTW(x_keypoint, y_keypoint, x_keypoint2, y_keypoint2):
    for i in range(len(Main.keypoint_name_list)):
        plt.rcParams["figure.figsize"] = (15, 8)
        #plt.rcParams['axes.grid'] = True
        plt.subplot(3, 5, i+1)
        plt.plot(x_keypoint[i], label=Main.keypoint_name_list[i]+'_x')
        plt.plot(x_keypoint2[i], label='Comp_'+Main.keypoint_name_list[i]+'_x')
        plt.legend()
        plt.ylim((0,1920))
    plt.show()
    for i in range(len(Main.keypoint_name_list)):
        plt.subplot(3, 5, i+1)
        plt.plot(y_keypoint[i], label=Main.keypoint_name_list[i]+'_y')
        plt.plot(y_keypoint2[i], label='Comp_' + Main.keypoint_name_list[i] + '_y')
        plt.legend()
        plt.ylim((0,1080))
    plt.show()



def Paint_Graph(x_keypoint, y_keypoint):
    for i in range(len(Main.keypoint_name_list)):
        plt.rcParams["figure.figsize"] = (15, 8)
        #plt.rcParams['axes.grid'] = True
        plt.subplot(3, 5, i+1)
        plt.plot(x_keypoint[i], label=Main.keypoint_name_list[i]+'_x')
        plt.legend()
        plt.ylim((0,1920))
    plt.show()
    for i in range(len(Main.keypoint_name_list)):
        plt.subplot(3, 5, i+1)
        plt.plot(y_keypoint[i], label=Main.keypoint_name_list[i]+'_y')
        plt.legend()
        plt.ylim((0,1080))
    plt.show()
