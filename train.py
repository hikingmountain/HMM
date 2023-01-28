from generate_samples import *

def estimate_transition_prob(samples, max_state):
    A = [[0] * max_state for i in range(max_state)]
    for sample in samples:
        prev_s = sample[0][0]
        for t in range(1, len(sample[0])):
            s = sample[0][t]
            A[prev_s][s] += 1
            prev_s = s

    for i in range(len(A)):
        normalize_array(A[i])

    return A


def estimate_pi(samples, max_state):
    pi = [0] * max_state
    for sample in samples:
        pi[sample[0][0]] += 1

    normalize_array(pi)

    return pi


def estimate_emission_prob(samples, max_state, max_observ):
    B = [[0] * max_observ for i in range(max_state)]
    for sample in samples:
        for t in range(len(sample[0])):
            s = sample[0][t]
            o = sample[1][t]
            B[s][o] = B[s][o] + 1

    for i in range(len(B)):
        normalize_array(B[i])

    return B


def normalize_array(arr):

    sm = sum(arr)
    for i in range(len(arr)):
        arr[i] = arr[i]/sm


if __name__ == '__main__':
    samples = generate(5, 10, 100000)
    pi = estimate_pi(samples, 3)
    A = estimate_transition_prob(samples, 3)
    B = estimate_emission_prob(samples, 3, 4)

    print("PI = ")
    print(pi)
    print("\nA = ")
    for i in range(len(A)):
        print(A[i])

    print("\n B = ")
    for i in range(len(A)):
        print(B[i])
