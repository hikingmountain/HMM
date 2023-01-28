import random
import bisect

# 隐状态字典
MAP_STATE = {
    0: 'neutral',
    1: 'happy',
    2: 'unhappy',
}

# 观测事件字典
MAP_ACTIVITY = {
    0: 'reading',
    1: 'shopping',
    2: 'running',
    3: 'watching',
}

# 初始状态概率数组
PI = [0.7, 0.2, 0.1]

# 状态转移概率矩阵
A = [
    [0.5, 0.3, 0.2],
    [0.4, 0.5, 0.1],
    [0.6, 0.1, 0.3],
]

# 发射概率矩阵
B = [
    [0.4, 0.1, 0.2, 0.3],
    [0.2, 0.5, 0.1, 0.2],
    [0.1, 0.1, 0.6, 0.2],
]


def index2activity(idx):
    activity = []
    for i in idx:
        act = MAP_ACTIVITY[i]
        activity.append(act)

    return activity


def index2state(index):
    emo_list = []
    for i in index:
        emo_list.append(MAP_STATE[i])

    return emo_list


def sample_from(p):
    p_sorted, idx_sorted = sort_index(p)
    p2dis = []
    p2dis.append(p_sorted[0])
    sum = p_sorted[0]
    for i in range(1, len(p_sorted)):
        sum += p_sorted[i]
        p2dis.append(sum)

    a, b = 0, 1
    n = random.uniform(a, b)
    i = bisect.bisect_left(p2dis, n)
    val = idx_sorted[i]

    return val


def sort_index(lst):
    lst_idx = [i for i in range(len(lst))]
    idx_sorted = []
    lst_sorted = []

    for i in range(len(lst) - 1):
        min_idx = 0
        for j in range(1, len(lst_idx)):
            if lst[lst_idx[min_idx]] > lst[lst_idx[j]]:
                min_idx = j

        idx = lst_idx.pop(min_idx)
        idx_sorted.append(idx)
        lst_sorted.append(lst[idx])

    idx_sorted.append(lst_idx[0])
    lst_sorted.append(lst[lst_idx[0]])

    return lst_sorted, idx_sorted


def generate_one(length):
    y_x = [[-1] * length for i in range(2)]
    y_x[0][0] = sample_from(PI)  # 采样首个隐状态
    y_x[1][0] = sample_from(B[y_x[0][0]])  # 根据首个隐状态采样观测值
    for t in range(1, length):
        y_x[0][t] = sample_from(A[y_x[0][t - 1]])
        y_x[1][t] = sample_from(B[y_x[0][t]])

    return y_x


def generate(minLen, maxLen, num):
    """
    :param minLen: 样本序列最小长度
    :param maxLen: 样本序列最大长度
    :param num: 样本个数
    :return: 样本
    """
    seqs = []
    for i in range(num):
        length = random.randint(minLen, maxLen)
        y_x = generate_one(length)
        seqs.append(y_x)

    return seqs

def convert_index_to_word(mat):
    for yx in mat:
        emo = index2state(yx[0])
        act = index2activity(yx[1])
        print(" ".join(a + '/' + e for a, e in zip(act, emo)))


if __name__ == '__main__':
    mat = generate(5, 7, 2)
    convert_index_to_word(mat)
