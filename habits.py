#!/usr/bin/env python3
"""habit-streak: track daily habits and streaks from your terminal. No dependencies."""

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".habit_streak.json"


def load():
    try:
        return json.loads(DATA_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


def streak(days):
    """Count consecutive days ending today (or yesterday, so a streak isn't lost before you check in)."""
    done = set(days)
    day = date.today()
    if day.isoformat() not in done:
        day -= timedelta(days=1)
    count = 0
    while day.isoformat() in done:
        count += 1
        day -= timedelta(days=1)
    return count


def last_week(days):
    done = set(days)
    today = date.today()
    return "".join(
        "■" if (today - timedelta(days=i)).isoformat() in done else "·"
        for i in range(6, -1, -1)
    )


def cmd_add(data, name):
    if name in data:
        print(f"'{name}' already exists.")
        return
    data[name] = []
    save(data)
    print(f"Added habit '{name}'. Check in with: habits.py done {name}")


def cmd_done(data, name):
    if name not in data:
        print(f"No habit named '{name}'. Add it with: habits.py add {name}")
        return
    today = date.today().isoformat()
    if today in data[name]:
        print(f"Already checked in '{name}' today. 💪")
        return
    data[name].append(today)
    save(data)
    print(f"✅ '{name}' done! Streak: {streak(data[name])} day(s) 🔥")


def cmd_remove(data, name):
    if data.pop(name, None) is None:
        print(f"No habit named '{name}'.")
        return
    save(data)
    print(f"Removed '{name}'.")


def cmd_list(data):
    if not data:
        print("No habits yet. Start one with: habits.py add read")
        return
    width = max(len("habit"), *(len(n) for n in data))
    print(f"{'habit':<{width}}  last 7 days  streak")
    for name, days in sorted(data.items()):
        print(f"{name:<{width}}  {last_week(days)}      {streak(days)} 🔥")


def main():
    parser = argparse.ArgumentParser(description="Track daily habits and streaks.")
    sub = parser.add_subparsers(dest="cmd")
    for cmd, help_text in [("add", "start tracking a habit"),
                           ("done", "check in a habit for today"),
                           ("remove", "stop tracking a habit")]:
        sub.add_parser(cmd, help=help_text).add_argument("name")
    sub.add_parser("list", help="show all habits (default)")
    args = parser.parse_args()

    data = load()
    if args.cmd == "add":
        cmd_add(data, args.name)
    elif args.cmd == "done":
        cmd_done(data, args.name)
    elif args.cmd == "remove":
        cmd_remove(data, args.name)
    else:
        cmd_list(data)


if __name__ == "__main__":
    main()
