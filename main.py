import os
import sys
import subprocess

from filesystem import path, direct
from paths import Paths

import config
from tools import *

# TODO: logging

paths = Paths()


def save(srclst, destlst):
    for src in srclst:
        for dest in destlst:
            if os.path.isfile(src):
                path.copy(src, dest)
            elif os.path.isdir(src):
                direct.copy(src, dest)


def command(cmd):
    if cmd == "help":
        with open("README.md") as docs:
            print("\n" + docs.read() + "\n")
    elif cmd == "new location":
        location = r"" + input("input location of file(s): ").strip()
        if not ":" in location:
            location = os.path.join(os.getcwd(), location)
        if not os.path.exists(location):
            print("location does not exist")
            return
        paths.add_location(location)
        print("new location saved!")
        return location
    elif cmd == "locations":
        if locations := paths.get_locations():
            for location in locations:
                print(location)
            return locations
        else:
            print("locations list is empty")
            print("\tuse 'new location'")
            return []
    elif cmd == "set backup":
        backup = r"" + input("input backup: ").strip()
        if not ":" in backup:
            backup = os.path.join(os.getcwd(), backup)
        if not os.path.exists(backup):
            print("location does not exist")
            return
        paths.set_backup(backup)
        print("new backup saved!")
        return backup
    elif cmd == "backup":
        if backup := paths.get_backup():
            print(backup)
            return backup
        else:
            print("you haven't set backup yet")
            print("\tuse'new backup'")
            return None
    elif cmd == "save to flash-drive":
        symbol = input("flash drive's symbol: ").strip().upper()
        save(paths.get_locations(), f"{symbol}:\\")
    elif cmd == "save":
        save(paths.get_locations(), (paths.get_backup(),))
    elif cmd == "reset":
        command("locations")
        command("backup")
        paths.reset()
        print("all info reseted!")
    elif cmd == "search queries":
        directs = set()
        while (dir_ := input("where do we search? ").strip()) != "":
            if dir_ == "///locs":
                for location in paths.locations():
                    if os.path.isdir(location):
                        directs.add(location)
            elif os.path.isdir(dir_):
                directs.add(dir_)
        print()
        queries = set()
        while (query := input("query: ")) != "":
            queries.add(query)
        found = search.query(directs, queries)
        print("\n")
        for file in found["files"]:
            print(file)
        print("\n\nFILES FOUND:", found["cnt"])
        return found
    elif cmd == "recover":
        locations = list(paths.get_locations())
        if not locations:
            print("no location")
            print("\t\tuse'new location'")
        backup = paths.get_backup()
        if not backup:
            print("no backup")
            print("\t\tuse'set backup'")
        for location in locations:
            if os.path.isfile(location):
                with subprocess.Popen(
                    ["./tools/recovery/recover", location, backup],
                    stdout=subprocess.PIPE,
                ) as proc:
                    print(proc.stdout.read().decode("utf-8"), end="")
            elif os.path.isdir(location):
                locations.extend(direct.fulltree(location))
    else:
        print("invalid command")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:  # if commands have already been given via command line
        command(" ".join(sys.argv[1:]))
    else:
        while True:
            cmd = input(">> ")
            if cmd in config.EXIT:
                break
            command(cmd)
    paths.save_changes()
