#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time

from selenium import webdriver


DIMENSIONS = '1280x800'  # Default image dimensions width x height
WAIT = 2  # Default wait time to render web page


def get_browser() -> webdriver:
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    return webdriver.Firefox(options=options)


def capture(browser: webdriver, url: str, image: str, dimensions: str = DIMENSIONS, wait: int = WAIT) -> None:
    width, height = [int(dim) for dim in dimensions.split('x')]
    browser.set_window_size(width, height)
    browser.get(url)
    browser.set_window_rect(x=0, y=0, width=width, height=height)
    time.sleep(wait)
    browser.save_screenshot(image)


def main():
    parser = argparse.ArgumentParser(description='Create and download screenshot for URL.')
    parser.add_argument('url', metavar='URL', type=str, help='Web page URL')
    parser.add_argument('image', metavar='IMAGE', type=str, help='Image file name')
    parser.add_argument('--dimensions', '-d', type=str, default=DIMENSIONS)
    parser.add_argument('--wait', '-w', type=int, default=WAIT)

    args = parser.parse_args()
    browser = get_browser()
    capture(browser, args.url, args.image, args.dimensions, args.wait)
    browser.close()


if __name__ == '__main__':
    main()