#!/bin/python3

import io
import os
import sys
import requests
import zipfile
import os

print("WARNING: This will download the development version of the AtomicDEX-API (mm2)")
input("Press enter to Continue...")

def download_progress(url, fn):
    with open(fn, 'wb') as f:
        r = requests.get(url, stream=True)
        total = r.headers.get('content-length')

        if total is None:
            f.write(r.content)
        else:
            downloaded = 0
            total = int(total)
            for data in r.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write(f"\rDownloading {fn}: [{'#' * done}{'.' * (50-done)}] {done*2}%")
                sys.stdout.flush()
    sys.stdout.write('\n')
    return r


def get_short_hash(branch):
    url = f"https://api.github.com/repos/KomodoPlatform/atomicDEX-API/branches/{branch}"
    r = requests.get(url)
    try:
        resp = r.json()
        commit_sha = resp["commit"]["sha"]
        return commit_sha[:9]
    except:
        print(f"{branch} does not exist!")
        return

def get_mm2_url(branch="dev", opsys="linux"):
    if opsys == "linux":
        os_str = "Linux"
    elif opsys == "osx":
        os_str = "Darwin"
    elif opsys == "windows":
        os_str = "Windows_NT"
    else:
        print("Invalid OS, must be in ['linux', 'osx', 'windows']")
        return

    short_hash = get_short_hash(branch)
    fn = f"mm2-{short_hash}-{os_str}-Release.zip"

    if not os.path.exists(fn):
        zip_url = f"http://195.201.0.6/{branch}/{fn}"
        print(f"Downloading latest mm2 build from {branch} branch: {zip_url}")
        download_progress(zip_url, fn)
    else:
        print(f"Latest mm2 build from {branch} branch already downloaded...")

    print(f"run unzip {fn} to extract the dev version of the AtomicDEX-API (mm2)")

if __name__ == '__main__':

    if len(sys.argv) == 3:
        branch = sys.argv[1]
        os = sys.argv[2]
        get_mm2_url(branch, os)

    elif len(sys.argv) == 2:
        branch = sys.argv[1]
        get_mm2_url(branch)

    else:
        get_mm2_url()
