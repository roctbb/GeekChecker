import tornado.ioloop
import tornado.web
import importlib as imp
import sys
import os
import markdown2
import subprocess
import uuid


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            code = self.get_argument('code')
            checker = self.get_argument('checker')
            data = self.get_argument('input')
            pswd = self.get_argument('pswd', None)

            if pswd != "pswd":
                res = {"state": "general error", "error": "AUTH"}
                self.write(res)
                return

            filename = "code/" + str(uuid.uuid4()) + ".py"
            with open(filename, 'w') as tfile:
                tfile.write(code)
                tfile.write('\n')
                tfile.write(checker)
                tfile.write('\n')
            process = subprocess.Popen(['python3', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.stdin.write(data.encode('utf-8'))
            process.stdin.close()
            process.wait(timeout=3)
            errors = process.stderr.read().decode('utf-8')
            if len(errors) > 0:
                res = {"state": "error", "error": errors}
                self.write(res)
                return
            result = process.stdout.read().decode('utf-8')
            res = {"state": "success", "result": result}
            self.write(res)
        except Exception as e:
            res = {"state": "general error", "error": str(e)}
            self.write(res)



routes = [
    (r"/", MainHandler),
]

app = tornado.web.Application(routes, debug=True)
app.listen(8087)
tornado.ioloop.IOLoop.current().start()