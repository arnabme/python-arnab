#!/usr/bin/env python3

import shutil
from datetime import datetime

FSTAB_PATH = "/etc/fstab"

def backup_fstab():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{FSTAB_PATH}.bak.{timestamp}"
    shutil.copy2(FSTAB_PATH, backup_path)
    print(f"[INFO] Backup created at {backup_path}")
    return backup_path

def comment_vxfs_lines():
    try:
        with open(FSTAB_PATH, "r") as f:
            lines = f.readlines()

        updated_lines = []
        modified = False

        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "vxfs" in stripped.split():
                updated_lines.append("# " + line)
                modified = True
                print(f"[MODIFIED] {line.strip()}")
            else:
                updated_lines.append(line)

        if modified:
            backup_fstab()
            with open(FSTAB_PATH, "w") as f:
                f.writelines(updated_lines)
            print("[INFO] Updated /etc/fstab with commented vxfs lines.")
        else:
            print("[INFO] No vxfs entries found in /etc/fstab.")

    except PermissionError:
        print("[ERROR] Permission denied. Run this script as root.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    comment_vxfs_lines()
