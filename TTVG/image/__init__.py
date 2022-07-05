import io
import random

from PIL import ImageDraw
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")


class Screenshot:
    def __init__(self):
        self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self._driver.get('https://www.reddit.com')
        self._driver.add_cookie({'name': 'over18', 'value': '1', 'domain': 'reddit.com'})

    @staticmethod
    def _get_image(image_bytes, radius=10):
        im = Image.open(io.BytesIO(image_bytes))
        circle = Image.new('L', (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
        alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
        alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
        im.putalpha(alpha)
        return im

    def _scroll_to_element(self, element):
        self._driver.execute_script("return arguments[0].scrollIntoView(false);", element)

    def save_comment(self, url, ):
        self._driver.get('https://www.reddit.com' + url)
        comment = self._driver.find_element(By.CLASS_NAME, 'Comment')
        self._scroll_to_element(comment)
        imageFile = self._get_image(comment.screenshot_as_png, 10)
        imageFile.save(name)

    def save_title(self, url, name):
        self._driver.get('https://www.reddit.com' + url)
        title = self._driver.find_element(By.CSS_SELECTOR, '[data-test-id=post-content]')
        self._scroll_to_element(title)
        imageFile = self._get_image(title.screenshot_as_png, 10)
        imageFile.save(name)

    def close(self):
        self._driver.close()

    def __del__(self):
        self.close()


def test():
    s = Screenshot()
    s.save_comment('/r/AskReddit/comments/vrh6gt/comment/ievidka')
    s.save_title('/r/AskReddit/comments/vrh6gt/comment/ievidka')


if __name__ == '__main__':
    test()
