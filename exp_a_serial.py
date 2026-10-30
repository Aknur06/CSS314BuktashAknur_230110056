import time, math
from multiprocessing import Pool

def heavy_math(n):
    return sum(math.sin(i) * math.cos(i) for i in range(1, n))

def experiment(workers, total_chunks=16, chunk_size=500_000):
    t0 = time.perf_counter()
    time.sleep(0.40)
    with Pool(processes=workers) as pool:
        pool.map(heavy_math, [chunk_size] * total_chunks)
    return time.perf_counter() - t0

if __name__ == "__main__":
    t1 = experiment(1)
    print(f"P=1 | Runtime={t1:.3f}s | Speedup=1.00x | Karp-Flatt e=0.000")
    for p in [2, 4]:
        tp = experiment(p)
        sp = t1 / tp
        e = ((p * tp / t1) - 1.0) / (p - 1.0)
        print(f"P={p} | Runtime={tp:.3f}s | Speedup={sp:.2f}x | Karp-Flatt e={e:.3f}")