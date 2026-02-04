import json
from datetime import datetime, timedelta

# Example function on one way to work with the JSON API, events also include their duration, that way it is possible to determine if an event is currently active.

def main():
    # 1) Open your JSON file
    with open("event_api.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2) Use the data exactly as before
    bosses = data["bosses"] # <- Key for what data is pulled, in this case "bosses" goes through all the world bosses.

    now_utc = datetime.utcnow()
    print("Current UTC time:", now_utc.strftime("%H:%M"), "\n")

    # We'll accumulate all upcoming spawns in a list
    upcoming_spawns = []

    # 3) Build a list of (spawn_datetime, boss_name, waypoint)
    for boss_info in bosses:
        boss_name = boss_info["name"]
        waypoint = boss_info["waypoint"]  # if you have that field

        for t_str in boss_info["times_utc"]:
            hour, minute = map(int, t_str.split(":"))
            # Construct a datetime for 'today' in UTC
            spawn_time = now_utc.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If that spawn_time is already in the past, add 1 day
            if spawn_time < now_utc:
                spawn_time += timedelta(days=1)

            upcoming_spawns.append((spawn_time, boss_name, waypoint))

    # Sort by spawn_time ascending
    upcoming_spawns.sort(key=lambda x: x[0])

    # 4) Take the next 5
    next_two = upcoming_spawns[:5] # Change this number to display more.

    print("--- Next 2 boss spawns ---")
    for i, (dt, boss_name, waypoint) in enumerate(next_two, start=1):
        # Calculate minutes until it spawns
        diff_minutes = int((dt - now_utc).total_seconds() // 60)
        spawn_str = dt.strftime("%Y-%m-%d %H:%M UTC")

        print(f"{i}) Boss: {boss_name}")
        print(f"   Waypoint: {waypoint or '(none set)'}")
        print(f"   Spawns in ~{diff_minutes} minutes at {spawn_str}\n")


if __name__ == "__main__":
    main()
