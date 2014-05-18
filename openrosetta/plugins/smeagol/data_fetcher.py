# -*- coding: utf-8 -*-
from data_storage import DataStorage
import urllib2, urllib
from webob import datetime_utils
import os
from uuid import uuid1
import traceback
import zipfile


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


class DataFetcher(object):
    def __init__(self,):
        super(DataFetcher, self).__init__()
        self.file_dir = "/files/"
        self.ds = DataStorage("sqlite:///"+os.path.dirname(os.path.abspath(__file__)) + self.file_dir+"cache.db")

        print "Current Cache size: " + str(self.cache_folder_size(
            os.path.dirname(os.path.abspath(__file__)) + self.file_dir)) + " MB"

    def fetch_data(self, url_list):
        list = {}
        for url in url_list:
            list[url] = self.get_file(url)
        return list

    def cache_folder_size(self, folder):
        folder_size = 0
        for (path, dirs, files) in os.walk(folder):
            for file in files:
                filename = os.path.join(path, file)
                folder_size += os.path.getsize(filename)
        return folder_size / 1000000

    def get_file(self, url):
        #check if in chache
        data_dict = self.ds.retrieve_dict(url)
        headers = self.check_if_valid_file_last_update(url)
        if data_dict is not None and headers is not None:
            # get the fucking date from the header
            if datetime_utils.parse_date(headers['Last-Modified']) > datetime_utils.parse_date(data_dict['time']):
                self.download(url)
                for path in data_dict['path']:
                    os.remove(path)
                self.ds.remove_dict(url)
            else:
                return data_dict['path']
        else:
            return self.download(url)

    def generate_file_path(self):
        return os.path.dirname(os.path.abspath(__file__)) + self.file_dir + str(uuid1())

    def unzip(self, path, dirname, url):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        zfile = zipfile.ZipFile(path)
        for name in zfile.namelist():
            zfile.extract(name, dirname)
        zip_files = os.listdir(dirname)
        results = []
        for zip_file in zip_files:
            path = self.generate_file_path()
            os.rename(dirname +'/'+ zip_file, path)
            results.append(path)
        return  results


    def get_unzip_list(self, filename, type, url, data_dict):
        if type.find("zip") != -1:
            list_zips = self.unzip(filename, os.path.dirname(os.path.abspath(__file__)) + self.file_dir + 'zips', url)
            os.remove(data_dict['path'])
            self.ds.remove_dict(url)
            save_dict = dict(path=list_zips, time=data_dict['time'])
            self.ds.store_dict(url, save_dict)
            return list_zips
        else:
            return None


    def check_if_valid_file_last_update(self, url):
        try:
            response = urllib2.urlopen(HeadRequest(url)).info()
            if response['Content-Type'].find("application") != -1:
                return response  #response['Last-Modified']
        except:
            return None


    def download(self, url):
        headers = self.check_if_valid_file_last_update(url)
        if headers is not None:
            path = self.generate_file_path()
            save_dict = dict(path=path, time=headers['Last-Modified'])
            urllib.urlretrieve(url, path)
            unzip_result = self.get_unzip_list(path, headers['Content-Type'], url, save_dict)
            if unzip_result is None:
                self.ds.store_dict(url, save_dict)
                return [path]
            else:
                return unzip_result
        else:
            return None


    def test(self):
        print self.fetch_data(
            ["http://www.pagepersonnel.it/index.html", "http://upload.wikimedia.org/wikipedia/it/3/30/Ls_xterm.png",
             "http://gis.csi.it/repertorio/sitad_wgs84/DBPR10_ELEMIDRI/elemidri.zip", "http://www.google.it"])
        print "second_dictionary", self.ds.retrieve_dict("hhh")

