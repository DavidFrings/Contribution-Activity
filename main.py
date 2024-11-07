from PIL import Image
from datetime import datetime, timedelta
import subprocess
import random

commits_per_date = {}
width, height = 53, 7  # DON'T CHANGE 

commit_levels = [1, 2, 3, 4, 5]
weights = [40, 30, 15, 4, 1]

def add_commits(date, count):
    commits_per_date[date] = commits_per_date.get(date, 0) + count - 1
    print(commits_per_date)

def create_image_from_commits(start_date, commits_per_date):
    img = Image.new('L', (width, height), color=255)

    for commit_date_str, num_commits in commits_per_date.items():
        commit_date = datetime.strptime(commit_date_str, '%d-%m-%Y')
        days_diff = (commit_date - start_date).days
        week_offset = days_diff // 7
        day_of_week = days_diff % 7

        if 0 <= week_offset < width and 0 <= day_of_week < height:
            pixel_value = max(0, min(255, 255 - (num_commits * 51)))
            img.putpixel((week_offset, day_of_week), pixel_value)

    img.save('preview.png')
    print("Preview image saved as 'preview.png'.")

def main(img_name):
    year_choice = int(input("Enter the year to generate the pattern for (e.g. 2023): ").strip())
    base_date = get_start_date(year_choice)

    choice = input("Do you want to read from the image or generate a random pattern? (image/random): ").strip().lower()

    if choice == 'image':
        pixels = read_image(img_name)
    elif choice == 'random':
        pixels = generate_random_pattern()
    else:
        print("Invalid choice. Exiting.")
        return

    for week_offset, day, num_commits in pixels:
        commit_date = get_commit_date(base_date, week_offset, day)
        add_commits(commit_date.strftime('%d-%m-%Y'), num_commits)

    create_image_from_commits(base_date, commits_per_date)

    user_response = input("Do you want to proceed with the commits? (yes/no): ").strip().lower()
    if user_response == 'yes':
        create_commits_from_data()
    else:
        print("Commits aborted.")

def get_start_date(year):
    first_day_of_year = datetime(year, 1, 1)
    days_to_sunday = first_day_of_year.weekday()  # Monday is 0, Sunday is 6
    start_date = first_day_of_year - timedelta(days=days_to_sunday)
    return start_date

def read_image(img_name):
    im = Image.open(img_name).convert('L')
    
    if im.size != (width, height):
        print(f"Error: Image size {im.size} does not match expected size {width}x{height}.")
        return []

    pixels_to_color = []
    for i in range(im.width):
        for j in range(im.height):
            pix_val = im.getpixel((i, j))
            avg_darkness = 255 - pix_val
            commit_level = avg_darkness // 51

            if commit_level > 0:
                pixels_to_color.append((i, j, commit_level))

    print(f"Pixels to color from image: {pixels_to_color}")
    return pixels_to_color

def generate_random_pattern():
    pixels_to_color = []
    for i in range(width):
        for j in range(height):
            num_commits = random.choices(commit_levels, weights=weights)[0]
            if num_commits > 0:
                pixels_to_color.append((i, j, num_commits))

    return pixels_to_color

def get_commit_date(base_date, week_offset, day):
    return base_date + timedelta(weeks=week_offset, days=day)

def create_commit(date):
    date_str = date.strftime("%a %b %d %I:%M %Y +0700")
    with open("list.txt", "a") as f:
        f.write("Hello, World!\n")
    subprocess.run(["git", "add", "list.txt"])
    subprocess.run(["git", "commit", "-m", "commit"])
    subprocess.run(["git", "commit", "--amend", "-m", "commit", f'--date="{date_str}"'])

def create_commits_from_data():
    for date_str, num_commits in commits_per_date.items():
        commit_date = datetime.strptime(date_str, '%d-%m-%Y')
        for _ in range(num_commits):
            create_commit(commit_date)
    
    push_commits()

def push_commits():
    print("Pushing commits to remote repository...")
    subprocess.run(["git", "push"])
    print("Commits pushed to the remote repository.")

if __name__ == "__main__":
    main("template.png")