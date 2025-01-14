#!python3
# Mark Bykerk KauffmanO.
# Read in the Config.adict to get values to make connection to Learn Ultra and Panopto server.
# Parse command line for a full path to a video of the format /<full_path>/<course_uuid>.mp4.
# The course_uuid is expected to be a course on the Learn Ultra Server.
# Call the upload_and_create_link method to upload the video to Panopto server and create the link in the course.
# The Panopto server and Learn server are those specified in the Config.adict.
# Sample Use:
#   python upload_and_create_link.py --full-file-path ./fc005cb3865a486981f221bd24111007.mp4

import argparse
import datetime
import ntpath # so we can grab the basename off the end of the full-file-path.
import os
from panopto_oauth2 import PanoptoOAuth2
from panopto_uploader import PanoptoUploader
import time
import urllib3
import Config

class UploadAndCreateLink:
    def __init__(self):
        # self.learn_rest_fqdn = Config.adict['learn_rest_fqdn']
        # self.learn_rest_key = Config.adict['learn_rest_key']
        # self.learn_rest_secret = Config.adict['learn_rest_secret']
        self.ppto_server = Config.credenciales['ppto_server']
        self.ppto_folder_id = Config.credenciales['ppto_folder_id']
        self.ppto_client_id = Config.credenciales['ppto_client_id']
        self.ppto_client_secret = Config.credenciales['ppto_client_secret']
        self.ppto_username = Config.credenciales['ppto_username']
        self.ppto_password = Config.credenciales['ppto_password']      

    def upload_and_create_link(self, full_file_path):
        print("current date and time is..")
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime)
        print("file: " + full_file_path)
        ssl_verify = True
        basename = ntpath.basename(full_file_path)
        (course_name, ext) = os.path.splitext(basename)

        oauth2 = PanoptoOAuth2(self.ppto_server, self.ppto_client_id, self.ppto_client_secret, ssl_verify) 

        uploader = PanoptoUploader(self.ppto_server, ssl_verify, oauth2, self.ppto_username, self.ppto_password)
        video_link_url = uploader.upload_video(full_file_path, self.ppto_folder_id)

        print("current date and time is..")
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime)
    
def parse_argument():
    '''
    Argument definition and handling.
    '''
    parser = argparse.ArgumentParser(description='Upload a single video file to Panopto server. Create link in Learn.')
    parser.add_argument('--full-file-path', dest='full_file_path', required=True, help='Full path to the file, including the filename.extension')
   
    return parser.parse_args()


def main():
    '''
    Main method
    '''
    args = parse_argument()

    print("current date and time is..")
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)

    upload_creator = UploadAndCreateLink()
    upload_creator.upload_and_create_link(args.full_file_path)

    print("current date and time is..")
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)
