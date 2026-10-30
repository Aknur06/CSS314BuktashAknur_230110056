import multiprocessing as mp
import ctypes
import time
import json
import numpy as np

# Уменьшили число итераций для мгновенного выполнения
K = 300_000

def worker_unpadded(counter_array, worker_id, iterations):
    for _ in range(iterations):
        counter_array[worker_id] += 1

def worker_padded(counter_array, worker_id, iterations):
    idx = worker_id * 8
    for _ in range(iterations):
        counter_array[idx] += 1

def worker_privatized(counter_array, worker_id, iterations):
    local_count = 0
    for _ in range(iterations):
        local_count += 1
    counter_array[worker_id] = local_count

def run_experiment(worker_func, P, array_size):
    arr = mp.Array(ctypes.c_int64, array_size)
    processes = []
    t0 = time.perf_counter()
    for p in range(P):
        proc = mp.Process(target=worker_func, args=(arr, p, K))
        processes.append(proc)
        proc.start()
    for proc in processes:
        proc.join()
    t1 = time.perf_counter()
    return t1 - t0, sum(arr)

def karp_flatt(T1, TP, P):
    if P <= 1 or T1 <= 0:
        return 0.0
    Sp = T1 / TP
    return ((P / Sp) - 1.0) / (P - 1.0)

def main():
    max_procs = mp.cpu_count() or 4
    procs = [p for p in [1, 2, 4, 8] if p <= max_procs]
    if 1 not in procs:
        procs.insert(0, 1)

    t1_unpadded, _ = run_experiment(worker_unpadded, 1, 64)
    t1_padded, _ = run_experiment(worker_padded, 1, 64)

    with open("results/false_sharing_karp_flatt.tsv", "w") as f:
        f.write("P\tT_unpadded_sec\te_unpadded\tT_padded_sec\te_padded\tT_privatized_sec\n")
        
        for P in procs:
            t_un, _ = run_experiment(worker_unpadded, P, 64)
            t_pad, _ = run_experiment(worker_padded, P, 64)
            t_priv, _ = run_experiment(worker_privatized, P, 64)

            e_un = karp_flatt(t1_unpadded, t_un, P)
            e_pad = karp_flatt(t1_padded, t_pad, P)

            f.write(f"{P}\t{t_un:.6f}\t{e_un:.6f}\t{t_pad:.6f}\t{e_pad:.6f}\t{t_priv:.6f}\n")

    print("[INFO] False sharing benchmark complete. Saved to results/false_sharing_karp_flatt.tsv")

if __name__ == "__main__":
    main()