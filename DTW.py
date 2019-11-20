from dtw import dtw
import numpy as np
import Paint_Graph as pg


def DTW(data1, data2, keypoint_name=" "):
    ts1 = list(data1)
    ts2 = list(data2)

    if(len(ts1)==0):
        return 0

    x = np.array(ts1).reshape(-1, 1)
    y = np.array(ts2).reshape(-1, 1)

    euclidean_norm = lambda x, y: np.abs(x - y)

    d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=euclidean_norm)

    #pg.Paint_CostMatrix(acc_cost_matrix.T, path, keypoint_name)

    ts1_dtw = []
    for i in range(1,len(path[0])):
        if(i==1):
             ts1_dtw.append(ts1[path[0][0]])
        if(path[1][i-1]==path[1][i]):
            continue
        else:
            ts1_dtw.append(ts1[path[0][i]])

    #print(keypoint_name)
    # print('max-min : '+str(max(ts1_dtw)-min(ts1_dtw)))
    # print('max_min2 : '+str(max(ts2)-min(ts2)))
    # print('stddev : '+str(np.std(ts1_dtw)))
    # print('stddev2 : '+str(np.std(ts2)))
    # print('var : '+str(np.cov(ts1_dtw, ts2)[0][1]))
    #print('coef : '+str(np.cov(ts1_dtw,ts2)[0][1]/(np.std(ts1_dtw)*np.std(ts2))))
    #print(ts1_dtw)

    ts1_std = np.std(ts1_dtw)
    ts2_std = np.std(ts2)
    cov = np.cov(ts1_dtw, ts2)[0][1]
    if(ts1_std==0 or ts2_std==0):
        return 0
    if((ts1_std<=4 and max(ts1_dtw)-min(ts1_dtw)<20) and ts2_std<=4 and max(ts2)-min(ts2)<20):
        cov = 1
        ts1_std=1
        ts2_std=1
    corrcoef = round(cov/(ts1_std*ts2_std),1)
    #pg.Paint_ComparisonGraph(ts1, ts2, ts1_dtw, keypoint_name)

    #print('corrcoef : ', end='')
    return corrcoef