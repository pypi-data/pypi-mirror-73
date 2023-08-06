# wcap

Capture web pages as images using Selenium and the FireFox webdriver.

# Usage

    wcap --dimensions 1500x1100 --wait 5 https://ukealong.com/key/c/ img/c.png

# Installation

    pip install wcap

In order for `wcap` to work you need to install the [FireFox web browser](https://www.mozilla.org/firefox) and [geckodriver](https://github.com/mozilla/geckodriver). To install `geckodriver` download the release for your operating system from https://github.com/mozilla/geckodriver/releases and move the executable file to a directory that is included in your PATH environment variable.

## Authors

`wcap` was written by [Ramiro Gómez](https://ramiro.org/).