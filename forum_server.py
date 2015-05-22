import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import sqlite3
import os.path
from tornado.options import define, options
import string
import time
import os
import random

define("port", default=8888, help="run on the given port", type=int)

def _execute(query):
    dbpath = './test.db'
    conn = sqlite3.connect(dbpath)
    #cur = conn.execute(query)

    try:
        cursor = conn.execute(query)
        conn.commit()
        res = cursor.fetchall()
        return res
    except Exception as e:
        print 'Error executing query: ',str(e)

    conn.close()

def random_str(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        self.res = None
        getusername = self.get_argument("username")
        getpassword = self.get_argument("password")
        self.query = """SELECT password FROM AUTH WHERE USERNAME = '%s' """ %(getusername)
        try:
            self.res = _execute(self.query)[0][0]
        except:
            #self.redirect("/")
            wrong=self.get_secure_cookie("wrong")
            self.set_secure_cookie("wrong", str(int(wrong)+1))
            self.write('Incorrect Login. <br />Try again \
            <a href="/login">Login</a> ')#+str(wrong))
        else:
            wrong=0
            self.set_secure_cookie("wrong",str(1))
            self.write('Succesful Login')

        if self.res == getpassword:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect("/")
            
        else:
            self.write('Incorrect Attempts: %s'%wrong)
            #self.set_secure_cookie("wrong", str(int(wrong)+1))
            #self.write('Incorrect Login. <br />Try again <a href="/login">Login</a> '+str(wrong))


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class ForumHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.items = []
        self.usernames = []
        self.times = []
        self.query = """ SELECT * FROM FORUM WHERE post_type = 'parent' """
        self.res = _execute(self.query)
        self.render('post.html', posts=self.res)

    @tornado.web.authenticated
    def post(self):
        self.query = """ SELECT ID FROM FORUM  """
        self.cnt = max(_execute(self.query))[0] + 1
        self.post = self.get_argument('post_text')
        self.post_type = 'parent'
        #self.post_type = self.get_argument('post_type')
        #self.user = self.get_argument('username')
        self.user = self.current_user
        self.time = str(time.strftime('%d/%m/%y-%H:%M:%S'))
        self.query = """ INSERT INTO FORUM (ID,USERNAME,POST,TIME,POST_TYPE) VALUES('%d', '%s', '%s', '%s', '%s') """ %(self.cnt, self.user, self.post, self.time, self.post_type);
        print self.query
        _execute(self.query)
        self.write('Success! '+self.query)
        self.redirect("/forum")

class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('Upload/ Download Files Here..')
        self.items = []
        for filename in os.listdir("uploads/"):
            self.items.append(filename)
        self.render('upload.html',items=self.items)

    @tornado.web.authenticated
    def post(self):
        self.file1 = self.request.files['file1'][0]
        self.orig_fname = self.file1['filename']
        self.fname = random_str()+str(self.orig_fname)
        self.out_file = open('uploads/'+self.fname,'w')
        self.out_file.write(self.file1['body'])
        self.write('Upload Successful')
        self.redirect("/upload")

class DownloadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, filename):
        x = open("uploads/" + filename)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)
        self.finish(x.read())

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/login",
            'template_path': os.path.join(base_dir, "templates"),
            'static_path': os.path.join(base_dir, "static"),
            'debug':True,
            "xsrf_cookies": True,
        }
    
        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/", MainHandler, name="main"),
            tornado.web.url(r'/login', LoginHandler, name="login"),
            tornado.web.url(r'/logout', LogoutHandler, name="logout"),
            tornado.web.url(r'/forum', ForumHandler, name="forum"),
            tornado.web.url(r'/upload', UploadHandler, name="upload"),
            tornado.web.url(r'/upload/([A-Za-z0-9\_\.\-%]+)', DownloadHandler, name="download"),
        ], **settings)

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
