#!/usr/bin/env python

import urllib, urllib2
import subprocess

class gist():
    def __init__(self, login = None, token = None):
        self.gisturl = "http://gist.github.com/gists"
        
        if not login and not token:
            plogin = subprocess.Popen(
                ("git", "config", "--global", "github.user"),
                stdout=subprocess.PIPE)
            ptoken = subprocess.Popen(
                ("git", "config", "--global", "github.token"),
                stdout=subprocess.PIPE)
            login = plogin.communicate()[0].strip()
            token = ptoken.communicate()[0].strip()

            retcode = not plogin.returncode and not ptoken.returncode
            assert retcode, 'github.user, github.token is not set.'

        self.login = login
        self.token = token
    
    def create(self, txt, filename = ""):
        data = {
            "login" : self.login,
            "token" : self.token,
            "file_ext[gistfile1]"  : "",
            "file_name[gistfile1]" : filename,
            "file_contents[gistfile1]" : txt,
            }
        
        post = urllib.urlencode(data)
        urllib2.urlopen(self.gisturl, post)

    def mcreate(self, contents):
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
        r = urllib2.urlopen(self.gisturl, post)

        return r

if __name__ == "__main__":
    import sys
    import os.path
    
    if len(sys.argv) > 1:
        g = gist()
        print "[github.user] %s" % g.login

        contents = []
        for args in sys.argv[1:]:
            f = os.path.abspath(args)
            name = os.path.basename(f)
            print "@ %s" % name,
            
            fp = open(f)
            txt = fp.read()
            fp.close()
            
            contents.append((name, txt))
            print "."
        
        print "create:",
        pgist = g.mcreate(contents)
        print pgist.geturl()

        print "done."
    else:
        print "gist: no input files"
