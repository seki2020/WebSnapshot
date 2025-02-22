import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from utils.helpers import save_data
from PIL import Image

class WebScraper:
    def __init__(self, url):
        self.url = url

    def fetch_content(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        # 配置代理
        proxy = os.getenv('PROXY_URL')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            print(f"Fetching content from URL: {self.url}")  # 打印URL
            driver.get(self.url)
            html_content = driver.page_source

            # Adjust window size to capture the entire page
            total_height = driver.execute_script("return document.body.scrollHeight")
            driver.set_window_size(1920, total_height)

            # Create directory for screenshots
            screenshot_dir = 'screenshots'
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            # Generate file name based on current date and time
            current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = os.path.join(screenshot_dir, f'{current_datetime}.png')

            # Capture screenshot
            driver.save_screenshot(screenshot_path)

            # Convert PNG to JPG
            image = Image.open(screenshot_path)
            image = image.convert('RGB')
            jpg_path = os.path.join(screenshot_dir, f'{current_datetime}.jpg')
            image.save(jpg_path, 'JPEG')

            driver.quit()
            return html_content
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def parse_content(self, html_content):
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Extracting all text content
            return soup.get_text()
        else:
            return "Failed to fetch content"

    def run(self):
        html_content = self.fetch_content()
        data = self.parse_content(html_content)
        save_data(data, 'output.txt')  # Save as text file

if __name__ == "__main__":
    url = "https://findy-code.io/recommends?sort=newest"  # Replace with the target URL
    # url = "https://findy-code.io/companies/503/jobs/edqXaFfV4CO0z"  # Replace with the target URL
    # url = "https://example.com/"  # Replace with the target URL
    scraper = WebScraper(url)
    scraper.run()