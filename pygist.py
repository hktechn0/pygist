#!/usr/bin/env python

import urllib, urllib2

class gist():
    def __init__(self, login, token):
        self.gisturl = "http://gist.github.com/gists"
        self.login = login
        self.token = token
    
    def upload(self, txt, filename = ""):
        data = {
            "login" : self.login,
            "token" : self.token,
            "file_ext[gistfile1]"  : "",
            "file_name[gistfile1]" : filename,
            "file_contents[gistfile1]" : txt,
            }
        
        post = urllib.urlencode(data)
        urllib2.urlopen(self.gisturl, post)

if __name__ == "__main__":
    import sys
    import os.path
    
    from gist_conf import *
    
    if len(sys.argv) > 1:
        f = os.path.abspath(sys.argv[1])
        name = os.path.basename(f)

        fp = open(f)
        txt = fp.read()
        fp.close()

        g = gist(username, apitoken)
        g.upload(txt, name)
        print 'gist: upload "%s"' % name
    else:
        print "gist: no input files"
