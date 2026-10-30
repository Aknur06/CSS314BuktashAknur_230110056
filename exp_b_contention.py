import time
from multiprocessing import Process, Value, Lock

def contended_worker(shared_counter, lock, iterations):
    for _ in range(iterations):
        with lock:
            shared_counter.value += 1

def run_contended(p, total_increments=200_000):
    increments_per_worker = total_increments // p
    counter = Value('i', 0)
    lock = Lock()
    procs = [Process(target=contended_worker, args=(counter, lock, increments_per_worker)) for _ in range(p)]
    t0 = time.perf_counter()
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()
    assert counter.value == total_increments
    return time.perf_counter() - t0

if __name__ == "__main__":
    t1 = run_contended(1)
    print(f"P=1 | Runtime={t1:.3f}s | Speedup=1.00x | Karp-Flatt e=0.000")
    for p in [2, 4]:
        tp = run_contended(p)
        sp = t1 / tp
        e = ((p * tp / t1) - 1.0) / (p - 1.0)
        print(f"P={p} | Runtime={tp:.3f}s | Speedup={sp:.2f}x | Karp-Flatt e={e:.3f}")