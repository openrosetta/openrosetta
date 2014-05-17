# -*- coding: utf-8 -*-
from data_storage import DataStorage
import urllib2, urllib
from webob import datetime_utils
import os
from uuid import uuid1
import traceback

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


class DataFetcher(object):
    def __init__(self, db_file, file_dir):
        super(DataFetcher, self).__init__()
        self.ds = DataStorage(db_file)
        self.file_dir = file_dir

    def fetch_data(self, url_list):
        list={}
        for url in url_list:
            list[url]=self.download(url)
        return list

    def get_file(self, url):
        #check if in chache
        #
        print "something"

    def generate_file_path(self):
        return os.path.dirname(os.path.abspath(__file__)) + self.file_dir + str(uuid1())

    def unzip(self, filename):
        # unzip return list of files
        # delete original file
        print "";

    def download(self, url):
        try:
            response = urllib2.urlopen(HeadRequest(url))
            #print response.info()['Content-Type'], datetime_utils.parse_date(response.info()['Last-Modified']), '\n'
            if(response.info()['Content-Type'].find("application") != -1):
                path = self.generate_file_path()
                save_dict = dict(path=path, time=response.info()['Last-Modified'])
                urllib.urlretrieve(url, path)
                self.ds.store_dict(url, save_dict)
                return path
            else:
                return None

        except Exception :
            print 'generic exception: ' + traceback.format_exc()
            return None


    def test(self):
        print self.fetch_data(
            ["http://www.pagepersonnel.it/index.html", "http://upload.wikimedia.org/wikipedia/it/3/30/Ls_xterm.png",
             "http://gis.csi.it/repertorio/sitad_wgs84/DBPR10_ELEMIDRI/elemidri.zip", "http://www.google.it"])

