from charts import app
from flask import Flask
import webbrowser, sys, subprocess, multiprocessing, logging

class Chart(object):

    def __init__(self):
        super().__init__()
        self.app = app
    
    def start_web_app(self):
        try:
            self.app.run()
        except Exception as e:
            logging.exception(e)

    def start(self):
        url = 'http://localhost:5000'
        # multiprocessing.set_start_method('spawn')
        p = multiprocessing.Process(target=self.start_web_app, args=())
        p.start()
        if sys.platform == 'darwin':    # in case of OS X
            subprocess.Popen(['open', url])
        else:
            webbrowser.open_new_tab(url)
        p.join()
