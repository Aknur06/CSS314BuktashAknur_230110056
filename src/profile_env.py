import sys
import os
import json
import platform
import argparse
from salt import get_student_params

def profile_hardware():
    info = {
        "python_version": sys.version,
        "os_kernel": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "logical_cores": os.cpu_count() or 1,
        "physical_cores": os.cpu_count() or 1,
        "cache_line_bytes": 64
    }
    
    if platform.system() == "Linux" and os.path.exists("/proc/cpuinfo"):
        try:
            with open("/proc/cpuinfo", "r") as f:
                lines = f.readlines()
            models = [line.split(":")[1].strip() for line in lines if "model name" in line]
            if models:
                info["cpu_model"] = models[0]
        except Exception:
            pass

    return info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--student-id", type=str, required=True, help="8-digit Student ID")
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)

    salted = get_student_params(args.student_id)
    with open("results/salted_params.json", "w") as f:
        json.dump(salted, f, indent=4)

    host_info = profile_hardware()
    with open("results/host_profile.json", "w") as f:
        json.dump(host_info, f, indent=4)

    print("[INFO] Milestone 0 complete. Files generated in results/")

if __name__ == "__main__":
    main()