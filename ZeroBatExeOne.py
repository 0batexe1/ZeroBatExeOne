#!/usr/bin/env python3
import argparse
import subprocess
import os
from pathlib import Path

BANNER = r"""
  ____   _______       __       __      __  
 |  _ \ |  ___\ \     / /__  __| | ___ / _| 
 | |_) || |_   \ \   / / _ \/ _` |/ _ \ |_  
 |  _ < |  _|   \ \_/ /  __/ (_| |  __/  _| 
 |_| \_\|_|      \___/ \___|\__,_|\___|_|   

           ZeroBatExeOne
------------------------------------------------
Usage: python3 ZeroBatExeOne.py -d example.com [options]
"""

CRITICAL_PATTERNS = {
    "/admin": "Admin panel",
    "/login": "Login page",
    "/dashboard": "Dashboard",
    ".git": "Git repository",
    ".env": "Environment file",
    "/api": "API endpoint",
    "/graphql": "GraphQL endpoint",
    "/upload": "File upload endpoint",
    "?id=": "Potential ID param",
    "?file=": "Potential file param",
    "?redirect=": "Potential redirect param"
}

def run_cmd(cmd_list):
    try:
        output = subprocess.check_output(cmd_list, stderr=subprocess.DEVNULL).decode()
        return output.splitlines()
    except Exception:
        return []

def save_unique(file_path, data_list):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if os.path.exists(file_path):
        with open(file_path) as f:
            existing.update([x.strip() for x in f.readlines()])
    new = set(data_list) - existing
    with open(file_path, "a") as f:
        for line in new:
            f.write(line + "\n")
    return list(new)

def httpx_live_check(domains):
    tmp_file = "temp_httpx.txt"
    Path(tmp_file).unlink(missing_ok=True)
    with open(tmp_file, "w") as f:
        f.write("\n".join(domains))
    live = run_cmd([
        "httpx",
        "-l", tmp_file,
        "-silent",
        "-status-code",
        "-threads", "20",
        "-timeout", "10"
    ])
    live_filtered = [line.split(" ")[0] for line in live if any(code in line for code in ["200", "301", "302", "401", "403"])]
    os.remove(tmp_file)
    return live_filtered

def main():
    print(BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", required=True)
    parser.add_argument("-w", "--wordlist", default="/opt/SecLists/Discovery/Web-Content/raft-large-directories.txt")
    parser.add_argument("-t", "--threads", type=int, default=20)
    parser.add_argument("-p", "--depth", type=int, default=3)
    parser.add_argument("-T", "--timeout", type=int, default=10)
    parser.add_argument("--screenshot", action="store_true")
    args = parser.parse_args()

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # 1. Subdomain discovery
    subdomains = run_cmd(["subfinder", "-d", args.domain, "-silent"])
    subdomains += run_cmd(["assetfinder", args.domain])
    subdomains = list(set(subdomains))
    subdomains = save_unique(output_dir/"subdomains.txt", subdomains)

    # 2. Recursive pipeline
    processed = set()
    to_process = subdomains.copy()
    depth = 0
    max_depth = args.depth

    while to_process and depth < max_depth:
        next_level = []
        # HTTP live check
        to_process = httpx_live_check(to_process)
        for sub in to_process:
            if sub in processed:
                continue
            processed.add(sub)

            # Directory / Endpoint discovery
            dirs = run_cmd([
                "ffuf",
                "-u", f"https://{sub}/FUZZ",
                "-w", args.wordlist,
                "-t", str(args.threads),
                "-mc", "200,301,302,401,403"
            ])
            dirs = save_unique(output_dir/f"{sub}_dirs.txt", dirs)

            # URL Extraction
            urls = run_cmd(["waybackurls", sub])
            urls += run_cmd(["gau", sub])
            urls = save_unique(output_dir/f"{sub}_urls.txt", urls)

            # JS hidden parameters
            js_files = [u for u in urls if u.endswith(".js")]
            js_endpoints = []
            for js in js_files:
                js_endpoints += run_cmd(["linkfinder", "-i", js, "-o", "cli"])
            js_endpoints = save_unique(output_dir/f"{sub}_js_endpoints.txt", js_endpoints)

            # Critical URL detection
            critical_list = []
            for u in urls + js_endpoints:
                for pattern, desc in CRITICAL_PATTERNS.items():
                    if pattern in u:
                        critical_list.append(f"{u} : {desc}")
            save_unique(output_dir/"critical_urls.txt", critical_list)

            # Add newly found subdomains for next recursion
            for u in urls + js_endpoints:
                host = u.split("/")[2] if "://" in u else u
                if host not in processed:
                    next_level.append(host)

        to_process = list(set(next_level))
        depth += 1

    # Screenshots
    if args.screenshot:
        for sub in processed:
            run_cmd(["aquatone", "-url", f"https://{sub}"])

    print("[*] ZeroBatExeOne taraması tamamlandı!")

if __name__ == "__main__":
    main()
