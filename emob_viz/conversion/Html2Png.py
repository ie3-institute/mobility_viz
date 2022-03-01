import os
import re
import time
from selenium import webdriver


class Html2Png:
    def __init__(self, path: str):
        self.path = path
        self.browser = webdriver.Firefox()

    @staticmethod
    def _remove_file_ending(file_name: str) -> str:
        """
        Removes the file ending from file name
        :param file_name: the file name with possible ending
        :return: the file name without ending
        """
        return re.sub("\\.[\\w\\d]{3,4}", "", file_name)

    @staticmethod
    def _prepare_url(path: str, file_name: str) -> str:
        """
        Prepare the url of the input file (html page)
        :param path: directory path of the file
        :param file_name: name of the file, including extension
        :return: the absolute url
        """
        abs_path = os.path.abspath(f'{path}/{file_name}').replace("\\", "/")
        if os.name == 'nt':
            abs_path = "/" + abs_path
        return f'file://{abs_path}.html'

    def _screenshot(self, url: str, delay: int, target: str) -> None:
        """
        Take a screenshot of the given url
        :param url: the website to visit
        :param delay: delay between website visit and screenshot
        :param target: the target file
        """
        self.browser.get(url)
        time.sleep(delay)
        self.browser.save_screenshot(target)

    def convert(self, filename: str, remove: bool = False, delay: int = 2) -> None:
        """
        Converts a given html page to png by taking a screenshot
        :param filename: name of the file with or without file ending
        :param remove: remove html file after screenshot?
        :param delay: delay between opening of website and taking the screenshot
        """
        # Prepare the directory path for the source file
        file_name = self._remove_file_ending(filename)
        url = self._prepare_url(self.path, file_name)

        self._screenshot(url, delay, f'{self.path}/{file_name}.png')

        if remove:
            os.remove(f'{self.path}/{file_name}.html')

    def close(self):
        self.browser.quit()
