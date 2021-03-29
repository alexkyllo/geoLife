"""split_geolife.py
Split GeoLife dataset into one CSV file per user per month
"""
import os
from pathlib import Path
from itertools import repeat
from multiprocessing import Pool
import dotenv


def split_trajectory(trajectory):
    rows = []
    month = None
    with trajectory.open() as t:
        [t.readline() for i in range(6)]
        for line in t:
            # year, month, day
            date = line.split(",")[5].split("-")
            next_month = (int(date[0]), int(date[1]))
            if month == None:
                month = next_month
            if month != next_month:
                yield month, rows
                month = next_month
                rows = []
            rows.append(line.strip())
        yield month, rows


def split_by_month(trajectories):
    data = {}
    trajectories = list(trajectories)
    trajectories.sort()
    for trajectory in trajectories:
        for month, rows in split_trajectory(trajectory):
            if month not in data:
                data[month] = rows
            else:
                data[month] = data[month] + rows
    return data


def process_one_user(user_dir, output_dir):
    """"""
    user_id = user_dir.name
    user_output_dir = output_dir / Path(user_id)
    user_output_dir.mkdir(exist_ok=True)
    data = split_by_month((user_dir / Path("Trajectory")).glob("*"))
    for year, month in data.keys():
        rows = data[year, month]
        output_file = user_output_dir / Path(f"{year}_{month:02}.csv")
        print(f"Writing: {output_file}")
        with output_file.open(mode="w") as f:
            f.write("\n".join(rows) + "\n")


def split_user_months(input_dir, output_dir):
    output_dir.mkdir(exist_ok=True)
    user_dirs = Path(input_dir).glob("*")
    with Pool(os.cpu_count() // 2) as p:
        p.starmap(process_one_user, zip(user_dirs, repeat(output_dir)))


if __name__ == "__main__":
    dotenv.load_dotenv()
    INPUT_DIR = Path(os.getenv("GEOLIFE_DATA_DIR"))
    OUTPUT_DIR = INPUT_DIR / "user_by_month"
    split_user_months(INPUT_DIR, OUTPUT_DIR)