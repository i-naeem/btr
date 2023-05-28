import os
from dotenv import load_dotenv

load_dotenv()

CHROME_EXECUTABLE_PATH = os.environ.get('CHROME_EXECUTABLE_PATH') or "./assets/chromedriver.exe"

if __name__ == '__main__':
    print(CHROME_EXECUTABLE_PATH)
