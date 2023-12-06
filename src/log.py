import os, time


class MyLogger:
    def __init__(self, path):
        self.file = open('../log/log_file/{}'.format(path), 'a+')

    def log(self, text, display=False):
        self.file.write(text.strip() + '\n')
        if display:
            print(text)
        return

    def __del__(self):
        self.file.close()
