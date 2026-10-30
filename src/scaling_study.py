import time
import json
import os
import numpy as np
import multiprocessing as mp

def stencil_worker(chunk):
    return np.sum(chunk * 1.0001)

def run_strong_scaling(N, P):
    data = np.ones((N, N), dtype=np.float64)
    chunks = np.array_split(data, P)
    t0 = time.perf_counter()
    with mp.Pool(P) as pool:
        _ = pool.map(stencil_worker, chunks)
    t1 = time.perf_counter()
    return t1 - t0

def run_weak_scaling(N_base, P):
    N_P = int(np.ceil(N_base * np.sqrt(P)))
    data = np.ones((N_P, N_P), dtype=np.float64)
    chunks = np.array_split(data, P)
    t0 = time.perf_counter()
    with mp.Pool(P) as pool:
        _ = pool.map(stencil_worker, chunks)
    t1 = time.perf_counter()
    return t1 - t0

def main():
    with open("results/salted_params.json", "r") as f:
        params = json.load(f)
    
    N = params["N"]
    max_cores = os.cpu_count() or 4
    procs = [1, 2, 4, min(8, max_cores)]
    procs = sorted(list(set([p for p in procs if p <= max_cores])))

    t1_strong = run_strong_scaling(N, 1)

    with open("results/scaling_metrics.tsv", "w") as f:
        f.write("P\tT_strong_sec\tSpeedup_strong\tEfficiency_pct\tserial_fraction_s\tT_weak_sec\n")
        
        for P in procs:
            t_strong = run_strong_scaling(N, P)
            speedup = t1_strong / t_strong
            eff = (speedup / P) * 100.0
            
            s_frac = ((1.0 / speedup) - (1.0 / P)) / (1.0 - (1.0 / P)) if P > 1 else 0.0
            s_frac = max(0.0, s_frac)

            t_weak = run_weak_scaling(N, P)

            f.write(f"{P}\t{t_strong:.6f}\t{speedup:.4f}\t{eff:.2f}\t{s_frac:.6f}\t{t_weak:.6f}\n")

    flops = N * N
    dram_bytes = N * N * 8
    ai = flops / dram_bytes

    roofline = {
        "arithmetic_intensity_flops_per_byte": ai,
        "regime": "Memory-Bandwidth Bound" if ai < 1.0 else "Compute Bound",
        "notes": "Low arithmetic intensity indicates DRAM bandwidth limits performance."
    }

    with open("results/roofline_summary.json", "w") as f:
        json.dump(roofline, f, indent=4)

    print("[INFO] Scaling study complete. Saved to results/scaling_metrics.tsv")

if __name__ == "__main__":
    main()