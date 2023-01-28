import copy
import math
import sys

# 隐状态字典
MAP_STATE = {
    0: 'neutral',
    1: 'happy',
    2: 'unhappy',
}

# 观测事件字典
MAP_ACTIVITY = {
    'reading': 0,
    'shopping': 1,
    'running': 2,
    'watching': 3,
}

# 初始状态概率数组
pi = [math.log(0.7), math.log(0.2), math.log(0.1)]

# 状态转移概率矩阵
A = [
    [math.log(0.5), math.log(0.3), math.log(0.2)],
    [math.log(0.4), math.log(0.5), math.log(0.1)],
    [math.log(0.6), math.log(0.1), math.log(0.3)],
]

# 发射概率矩阵
B = [
    [math.log(0.4), math.log(0.1), math.log(0.2), math.log(0.3)],
    [math.log(0.2), math.log(0.5), math.log(0.1), math.log(0.2)],
    [math.log(0.1), math.log(0.1), math.log(0.6), math.log(0.2)],
]

def activity2index(activity):
    idx = []
    for act in activity:
        i = MAP_ACTIVITY[act]
        idx.append(i)

    return idx

def index2state(index):
    emo_list = []
    for i in index:
        emo_list.append(MAP_STATE[i])

    return emo_list

def predict(activity):
    seq_len = len(activity)     # 序列长度
    num_state = len(MAP_STATE)      # 状态个数
    psi = [ [0] * len(MAP_STATE) for i in range(seq_len) ]      # 前驱数组
    score = [0] * num_state     # 最优局部路径的概率值
    act_idx = activity2index(activity)

    # 步骤一：t=1时
    for cur_s in range(num_state):
        score[cur_s] = pi[cur_s] + B[cur_s][act_idx[0]]


    # 步骤二：t>=2时，递推
    for t in range(1, seq_len):
        pre_score = copy.deepcopy(score)

        for cur_s in range(num_state):

            score[cur_s] = -sys.maxsize - 1
            # 搜索概率最大路径，保存前驱结点编号
            for pre_s in range(num_state):
                p = pre_score[pre_s] + A[pre_s][cur_s] + B[cur_s][act_idx[t]]
                if score[cur_s] < p:
                    score[cur_s] = p
                    psi[t][cur_s] = pre_s

    # 步骤三：回溯，求全局最优路径
    path_idx = []
    node_idx = score.index(max(score))
    for t in range(seq_len-1, -1, -1):
        path_idx.append(node_idx)
        node_idx = psi[t][node_idx]

    path_idx.reverse()

    emo_state = index2state(path_idx)

    return activity, emo_state


if __name__ == '__main__':
    activity = ['reading', 'watching', 'running', 'reading', 'watching', 'shopping', 'watching']
    act, emo = predict(activity)
    print(act)
    print(emo)










