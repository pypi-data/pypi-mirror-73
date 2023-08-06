#!/usr/bin/env python
import re
import os
import sys
import json
import argparse
import urllib.error
import urllib.request

__version__ = '4.4.4'

def dl(url):
    req = urllib.request.Request(url, headers = {'User-Agent':'Mozilla/5.0'})

    try:
        response = urllib.request.urlopen(req)

    except urllib.error.URLError as e:
        exit('\033[1;31;40mError downloading data \033[1;33;40m({})'.format(e.reason if hasattr(e, 'reason') else e.code))

    except:
        exit('\033[1;31;40mError downloading data')

    return response

def main():
    parser = argparse.ArgumentParser(description = '\n \033[1;32;40m|M|a|h|i|m|\n\033[1;31;40m_______ \n\n\n\033[1;32;40mBy : Mazidul \n \033[1;35;40mhttps://github.com/mahim4\033[1;32;40m')

    parser.add_argument('url', help = '\033[1;31;40mInstagram image/video post link\033[1;32;40m')
    parser.add_argument('-q', '--quiet', action = 'store_true', help = '\033[1;31;40mSilence output\033[1;32;40m')
    parser.add_argument('-d', '--debug', action = 'store_true', help = '\033[1;31;40mSave json data for debug\033[1;32;40m')
    parser.add_argument('-p', '--path', metavar = 'PATH', help = '\033[1;31;40mSpecify download path')

    args = parser.parse_args()

    if args.quiet:
        sys.stdout = sys.stderr = open(os.devnull, 'w')

    if args.path and not os.path.exists(args.path):
        os.makedirs(args.path)

    print('\033[1;31;40m         +-+-+-+-+-+ \n\033[1;32;40m         |M|a|h|i|m| \n \033[1;33;40m        +-+-+-+-+-+ \n \033[1;34;40m        By : Mazidul \n \033[1;35;40m  https://github.com/mahim4\n\033[1;32;40mDownloading \033[1;33;40m{} \033[1;32;40m'.format(args.url))

    file_path = os.path.abspath(args.path) if args.path else os.getcwd()

    url_id = args.url.rstrip('/').split('/')[-1]

    url_response = dl(args.url)

    html_lines = url_response.read().decode().splitlines()

    for html_line in html_lines:
        if '_sharedData = ' in html_line:
            json_data = json.loads(html_line.split('_sharedData = ')[1][:-10])

    if not 'json_data' in locals():
        exit('\033[1;31;40mError no data found')

    if args.debug:
        file_name = '{}/{}.json'.format(file_path, url_id)

        with open(file_name, 'w') as f:
            json.dump(json_data, f)

        print('\033[1;32;40m Saved ')

    json_data = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    json_content = []

    if 'edge_sidecar_to_children' in json_data:
        for e in json_data['edge_sidecar_to_children']['edges']:
            json_content.append(e['node'])

    else:
        json_content.append(json_data)

    for i, c in enumerate(json_content):
        file_url = c['video_url'] if c['is_video'] else c['display_url']
        file_ext = 'mp4' if c['is_video'] else 'jpg'
        file_num = str(-(i+1)) if len(json_content) > 1 else ''

        file_name = '{}/{}{}.{}'.format(file_path, url_id, file_num, file_ext)

        url_response = dl(file_url)

        with open(file_name, 'wb') as f:
            f.write(url_response.read())

        print('\033[1;32;40mSaved')

if __name__ == '__main__':
    main()
