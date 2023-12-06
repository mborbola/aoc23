import requests
import sys
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def download_url_content(url, cookies):
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def main(year, day_range):
    # Parse the day range argument
    if '-' in day_range:
        start_day, end_day = map(int, day_range.split('-'))
    else:
        start_day = end_day = int(day_range)

    cookies = {'session': os.getenv('SESSION_ID')}

    for day in range(start_day, end_day+1):
        exercise_url = f"https://adventofcode.com/{year}/day/{day}"
        exercise_html = download_url_content(exercise_url, cookies)
        soup = BeautifulSoup(exercise_html, 'html.parser')

        exercise_texts = []

        article_tags = soup.findAll('article', {'class': "day-desc"})
        for tag in article_tags:
            for h2_tag in tag.select("h2"): 
                h2_tag.extract()
            text = tag.getText() 
            exercise_texts.append(text)

        input_url = f"https://adventofcode.com/{year}/day/{day}/input"
        input_text = download_url_content(input_url, cookies)

        dirname = str(day) # directory name for day
        if not os.path.exists(dirname): # check if directory exists
            try:
                os.makedirs(dirname) # create it if it doesn't exist
            except OSError as e:
                print(e)

        for index, exercise_text in enumerate(exercise_texts):
            exercise_filename = f"Part_{index+1}.txt"
            path = os.path.join(dirname, exercise_filename)
            with open(path, "w") as file:
                file.writelines(exercise_text)
        
        input_filename = "input.txt"
        path = os.path.join(dirname, input_filename)
        with open(path, "w") as file:
            file.writelines(input_text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.py <year> <day range>")
        sys.exit(1)

    year = sys.argv[1]
    day_range = sys.argv[2]

    main(year, day_range)