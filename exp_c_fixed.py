import time
from multiprocessing import Pool

def private_worker(iterations):
    local_sum = 0
    for _ in range(iterations):
        local_sum += 1
    return local_sum

def run_privatized(p, total_increments=5_000_000):
    increments_per_worker = total_increments // p
    tasks = [increments_per_worker] * p
    t0 = time.perf_counter()
    with Pool(processes=p) as pool:
        results = pool.map(private_worker, tasks)
    total = sum(results)
    assert total == total_increments
    return time.perf_counter() - t0

if __name__ == "__main__":
    t1 = run_privatized(1)
    print(f"P=1 | Runtime={t1:.3f}s | Speedup=1.00x | Karp-Flatt e=0.000")
    for p in [2, 4]:
        tp = run_privatized(p)
        sp = t1 / tp
        e = ((p * tp / t1) - 1.0) / (p - 1.0)
        print(f"P={p} | Runtime={tp:.3f}s | Speedup={sp:.2f}x | Karp-Flatt e={e:.3f}")