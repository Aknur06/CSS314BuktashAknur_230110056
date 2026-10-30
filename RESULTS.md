# Performance Diagnostics & Karp-Flatt Analysis
Student ID: 230110056

| Experiment Mode | T1 (s) | T2 (s) | T4 (s) | e(2) | e(4) | Architectural Diagnosis |
|---|---|---|---|---|---|---|
| A: Serial Tail | 3.20 | 1.80 | 1.10 | 0.125 | 0.120 | Constant e - Fixed Amdahl serial path |
| B: Lock Contention | 0.65 | 1.10 | 2.40 | 1.380 | 3.920 | Surging e - Lock thrashing & coherence traffic |
| C: Privatized State | 0.40 | 0.21 | 0.11 | 0.020 | 0.015 | Collapsed e - Linear scalability restored |