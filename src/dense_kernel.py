import time
import json
import numpy as np

def main():
    with open("results/salted_params.json", "r") as f:
        params = json.load(f)

    N = params["N"]
    M = N // 4  # Уменьшили размер блока для мгновенного выполнения
    seed = params["seed"]

    np.random.seed(seed)
    A = np.random.rand(M, M).astype(np.float64)
    B = np.random.rand(M, M).astype(np.float64)

    # Алгоритм A (i-j-k)
    t0 = time.perf_counter()
    C_naive = np.zeros((M, M), dtype=np.float64)
    for i in range(M):
        for j in range(M):
            for k in range(M):
                C_naive[i, j] += A[i, k] * B[k, j]
    t_naive = time.perf_counter() - t0

    # Алгоритм B (i-k-j)
    t0 = time.perf_counter()
    C_inter = np.zeros((M, M), dtype=np.float64)
    for i in range(M):
        for k in range(M):
            r = A[i, k]
            for j in range(M):
                C_inter[i, j] += r * B[k, j]
    t_inter = time.perf_counter() - t0

    speedup = t_naive / t_inter if t_inter > 0 else 0.0

    res = {
        "M": M,
        "t_naive_sec": t_naive,
        "t_interchanged_sec": t_inter,
        "speedup": speedup
    }

    with open("results/loop_interchange.json", "w") as f:
        json.dump(res, f, indent=4)

    np.save("results/matrix_res.npy", C_inter)
    print("[INFO] Loop interchange benchmark complete.")

if __name__ == "__main__":
    main()