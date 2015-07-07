#!/usr/bin/env python3

# credits to Nathan Henrie for the most part of this code, which I shamelessly stole from here:
# http://n8henrie.com/2014/05/decrypt-chrome-cookies-with-python/

import sqlite3
import os.path
import urllib.parse
import sys
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
 
# Strip padding by taking off number indicated by padding
# eg if last is '\x0e' then ord('\x0e') == 14, so take off 14.
# You'll need to change this function to use ord() for python2.
def clean(x):
    return x[:-x[-1]].decode('utf8')

def chrome_decrypt(encrypted_value, iv, key=None):
 
        # Encrypted cookies should be prefixed with 'v10' according to the
        # Chromium code. Strip it off.
        encrypted_value = encrypted_value[3:]
 
        cipher = AES.new(key, AES.MODE_CBC, IV=iv)
        decrypted = cipher.decrypt(encrypted_value)
        #print(decrypted)
        return clean(decrypted)

#default pass only valid for linux
def chrome_cookies(url, cookie_file, my_pass = 'peanuts'.encode('utf8') ):
 
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16
 
    iterations = 1003 # it's 1 for linux

    # Generate key from values above
    key = PBKDF2(my_pass, salt, length, iterations)
 
    # Part of the domain name that will help the sqlite3 query pick it from the Chrome cookies
    #domain = urlparse.urlparse(url).netloc
    domain = urllib.parse.urlparse(url).netloc
    domain_no_sub = '.'.join(domain.split('.')[-2:])
 
    #sql = c.execute("select host_key,name,value,path,expires_utc,secure,httponly,persistent from cookies where host_key like '%.google.com%'")

    conn = sqlite3.connect(cookie_file)
    #sql = 'select name, value, encrypted_value from cookies where host_key like "%{}%"'.format(domain_no_sub)
 
    sql =  'select name,value, encrypted_value, host_key, path,expires_utc,secure,httponly,persistent from cookies where host_key like "%{}%"'.format(domain_no_sub)

    #cookies = {}
    cookies_list = []
 
    with conn:
        for k, v, ev, host, path, exp, sec, httponly, session in conn.execute(sql):
 
            # if there is a not encrypted value or if the encrypted value
            # doesn't start with the 'v10' prefix, return v
            if v or (ev[:3] != b'v10'):
                value = v
            else:
                value = chrome_decrypt(ev, iv, key=key)
                #decrypted_tuple = (k, chrome_decrypt(ev, iv,    key=key))
                #cookies_list.append(decrypted_tuple)
            cookie = {
                'name': k,
                'value': value,
                'domain' : host,
                'path' : path,
                'httpOnly' : bool(httponly),
                'secure' : bool(sec),
            }
            cookies_list.append(cookie)
        #cookies.update(cookies_list)
            
    return cookies_list


def main():
    if len(sys.argv) < 3:
        print("usage: %s <url> <cookie_file> <keyfile>" % sys.argv[0])
        sys.exit(-1)
    url = sys.argv[1]
    cookie_file = sys.argv[2]
    keyfile = sys.argv[3]

    key = open(keyfile).read().encode('ascii')
    cookies = chrome_cookies(url, cookie_file, my_pass=key)
    #now we need to convert to json for import
    print(json.dumps(cookies, indent=)4)


main()
