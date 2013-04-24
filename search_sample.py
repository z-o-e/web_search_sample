"""
Created on Fri Mar 23 07:21:26 2013
Modified on Sat Mar 24 08:06:33 2013

@author: huiyingzhang

This script extracts urls from university of virginia's web index
and compare the google search result.
"""

import re
import urllib2
import sys
import BaseHTTPServer
from xgoogle.search import GoogleSearch, SearchError


def retrieve_web_page(addr):
    try:
        web_handle=urllib2.urlopen(addr)
    except urllib2.HTTPError,e:
        error_desc=BaseHTTPServer.BaseHTTPRequestHandler.response[e.code][0]
        print "Cannot retrieve URL: HTTP Error Code", e.code
        sys.exit(1)
    except urllib2.URLError,e:
        print "Cannot retrieve URL:"+ e.reason[1]
        sys.exit(1)
    except:
        print "Cannot retrieve URL: unknown error"
        sys.exit(1)
    return web_handle

#store urls from uva web index
def store_urls(website_text):
    uva_list=[]
    f1=open('uvasearch.txt','w')
    for match in re.finditer(r'(href="http://)([\w\.-_]+)(virginia.edu)([\w\.-_]*)',website_text):
        clipped=re.search('(href=")(http://[\w\.-_]+)',match.group(0))
        f1.write(clipped.group(2)+'\n')
        uva_list.append(clipped.group(2))
    f1.close()
    return sorted(uva_list)

handle=retrieve_web_page("http://www.virginia.edu/atoz/")
website_text=handle.read()
uva_list=store_urls(website_text)

#strap related urls from google
try:
    gs=GoogleSearch("University of Virginia")
    gs.results_per_page=25
    search_list=[]
    f2=open('googlesearch.txt','w')
    for page in range(0,5):
        gs.page=page
        results=gs.get_results()
        for result in results:
            search_list.append(result.url.encode('utf8'))
            f2.write(result.url.encode('utf8')+'\n')
    f2.close()
except SearchError, e:
    sys.exit(1)

#compare two 
common=set(search_list).intersection(set(uva_list))
