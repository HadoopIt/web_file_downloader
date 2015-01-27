# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 14:57:12 2014

@author: Bing Liu
"""

import lxml.html, urllib2, urlparse, os
import sys

def main(base_url, file_type, save_dir):    
    # fetch the page
    res = urllib2.urlopen(base_url)
    
    # parse the response into an xml tree
    tree = lxml.html.fromstring(res.read())
    
    # construct a namespace dictionary to pass to the xpath() call
    # this lets us use regular expressions in the xpath
    ns = {'re': 'http://exslt.org/regular-expressions'}
    
    # iterate over all <a> tags whose href ends in ".pdf" (case-insensitive)
    for node in tree.xpath('//a[re:test(@href, "\.' + file_type + '$", "i")]', namespaces=ns): 
        # print the href, joining it to the base_url
        file_url =  urlparse.urljoin(base_url, node.attrib['href'])
        print 'Downloading %s...' % file_url.split('/')[-1]
        download_file = urllib2.urlopen(file_url)
        data = download_file.read()
        with open(save_dir + '/' + file_url.split('/')[-1], "wb") as f:
            f.write(data)
    print 'All DONE!'

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python web_file_downloader.py <webpage-url> <file_type> <save-dir>'
        sys.exit()
    url = sys.argv[1]
    file_type = sys.argv[2]
    save_dir = sys.argv[3]
    
    if os.path.exists(save_dir) is False:
        os.mkdir(save_dir)
    main(url, file_type, save_dir)
