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

    def multiupload(self, contents):
        data = {
            "login" : self.login,
            "token" : self.token,
            }

        if isinstance(contents, dict):
            contents = contents.items()

        i = 1
        for f in contents:
            p = "[gistfile%d]" % i
            data["file_ext" + p] = ""
            data["file_name" + p] = f[0]
            data["file_contents" + p] = f[1]
            i += 1

        post = urllib.urlencode(data)
        urllib2.urlopen(self.gisturl, post)

if __name__ == "__main__":
    import sys
    import os.path
    
    from gist_conf import *
    
    if len(sys.argv) > 1:
        print 'gist: upload'

        contents = []
        for args in sys.argv[1:]:
            f = os.path.abspath(args)
            name = os.path.basename(f)
            print "> %s" % name,
            
            fp = open(f)
            txt = fp.read()
            fp.close()

            contents.append((name, txt))
            print "."
            
        g = gist(username, apitoken)
        g.multiupload(contents)
        print "done."
    else:
        print "gist: no input files"
