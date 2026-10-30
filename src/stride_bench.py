import time
import json
import numpy as np

def main():
    with open("results/salted_params.json", "r") as f:
        params = json.load(f)

    buffer_elements = params["buffer_elements"]
    data = np.ones(buffer_elements, dtype=np.float64)
    strides = [1, 2, 4, 8, 16, 32, 64, 128]

    with open("results/stride_results.tsv", "w") as f:
        f.write("stride\ttime_ns\tlatency_per_element_ns\n")
        
        for s in strides:
            for _ in range(5):
                _ = np.sum(data[::s])
            
            times = []
            for _ in range(5):
                t0 = time.perf_counter_ns()
                _ = np.sum(data[::s])
                t1 = time.perf_counter_ns()
                times.append(t1 - t0)
            
            median_ns = float(np.median(times))
            elements_touched = buffer_elements // s
            latency_ns = median_ns / elements_touched
            
            f.write(f"{s}\t{median_ns:.2f}\t{latency_ns:.4f}\n")

    print("[INFO] Stride benchmark complete.")

if __name__ == "__main__":
    main()