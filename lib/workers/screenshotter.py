import base64
import os
import subprocess
import tempfile


class Screenshotter:

    def __init__(self):
        self.chrome = self.locate_chrome()

    def read_image_base64(self, image_path: str):
        data = self.read_image(image_path)
        b64_data = base64.standard_b64encode(data)
        return b64_data


    def read_image(self, image_path: str):
        # TODO: Add Try Catch
        with open(image_path, mode="rb") as f:
            data = f.read()
        return data


    def locate_chrome(self):
        paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-beta",
            "/usr/bin/google-chrome-unstable",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        ]
        for path in paths:
            exists = os.path.isfile(path)
            if exists:
                return path

        return []

    def screenshot(self, protocol, host, port, path):
        full_url = self.__generate_url(protocol, host, port, path)
        b64_screenshot = self.__take_screenshot(full_url)


    def __generate_url(protocol, host, port, path):
        return protocol + '://' + host + ':' + str(port) + path # TODO: normalize path

    def __take_screenshot(self, url: str,):
        # TODO: sanity checks
        temp_dir = tempfile.mkdtemp(prefix="octopus_")
        temp_filename = temp_dir + "\\" + "screenshot.png"


        chrome_command_line = [self.chrome, "--headless", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                               "--disable-notifications",
                               "--no-first-run", "--disable-crash-reporter", "--ignore-certificate-errors", "--incognito",
                               "--disable-infobars", "--disable-sync", "--no-default-browser-check",
                               "--user-data-dir=" + temp_dir, "--screenshot=" + temp_filename, "--no-sandbox", "--enable-logging" ,url]

        # Since we cannot run chrome as root with sandbox
        # TODO: checks
        # if os.Geteuid() == 0:
        #   chromeArguments.append("--no-sandbox")
        p = subprocess.run(chrome_command_line, timeout=10)
        b64_screenshot = read_image_base64(temp_filename)
        #shutil.rmtree(temp_dir) # TODO: it returns Access Denied
        return b64_screenshot
