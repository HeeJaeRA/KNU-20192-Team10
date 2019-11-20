from dtw import dtw
import numpy as np
import Paint_Graph as pg


def DTW(data1, data2, keypoint_name=" "):
    ts1 = list(data1)
    ts2 = list(data2)

    x = np.array(ts1).reshape(-1, 1)
    y = np.array(ts2).reshape(-1, 1)

    euclidean_norm = lambda x, y: np.abs(x - y)

    d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=euclidean_norm)
    #print(d)

    #pg.Paint_CostMatrix(acc_cost_matrix.T, path, keypoint_name)

    ts1_dtw = []
    for i in range(1,len(path[0])):
        if(i==1):
             ts1_dtw.append(ts1[path[0][0]])
        if(path[1][i-1]==path[1][i]):
            continue
        else:
            ts1_dtw.append(ts1[path[0][i]])

    #pg.Paint_ComparisonGraph(ts1, ts2, ts1_dtw, keypoint_name)

    corrcoef = np.corrcoef(ts1_dtw, ts2)[1][0]
    return corrcoef
