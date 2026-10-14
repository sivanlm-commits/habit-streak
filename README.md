# 🔥 habit-streak

Track daily habits and streaks from your terminal — one Python file, zero dependencies.

```
habit     last 7 days  streak
exercise  ··■■■■■      5 🔥
read      ■■■■■■■      7 🔥
```

## Usage

```bash
python3 habits.py add read       # start tracking a habit
python3 habits.py done read      # check in for today
python3 habits.py                # see all habits, last 7 days, and streaks
python3 habits.py remove read    # stop tracking a habit
```

Your data is saved to `~/.habit_streak.json`.

## Ideas / contributing

Pull requests welcome! Some ideas:
- A `--date` option to check in for a past day
- Longest-ever streak
- Colored output

## License

MIT
