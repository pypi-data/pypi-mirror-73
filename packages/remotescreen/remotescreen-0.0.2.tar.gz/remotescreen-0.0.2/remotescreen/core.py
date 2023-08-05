import io
import os
import time
from PIL import ImageGrab
from omnitools import b64e
import threading
import tornado.ioloop
import tornado.web


__ALL__ = ["RemoteScreenServer"]


def take_screenshot():
    tmp = io.BytesIO()
    screenshot = ImageGrab.grab()
    screenshot.save(tmp, format="JPEG")
    tmp.seek(0)
    return tmp.read()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        style = '''<style>
body {
    margin: 0;
    padding: 0;
}
div#screenshot {
    text-align: center;
}
div#screenshot img {
    height: 100%;
}
</style>'''
        script = '''<script>
function get_screenshot() {
    var xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        var response = xhr.response;
        var src = "data:image/png;base64,"+response;
        document.querySelector("div#screenshot").innerHTML = "<img src='"+src+"' />";
    }
    xhr.open("GET", "/screenshot");
    xhr.send();
}
setInterval(get_screenshot, 2/3*1000);
</script>'''
        self.write('''{}<div id="screenshot"></div>{}'''.format(style, script))


class ScreenshotHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(b64e(take_screenshot()))


class ExitHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<script>window.close();</script>''')
        def job():
            time.sleep(1)
            os._exit(0)
        threading.Thread(target=job).start()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/screenshot", ScreenshotHandler),
        (r"/stop", ExitHandler),
    ])


def RemoteScreenServer():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()



