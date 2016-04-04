#!/usr/bin/env python
"""
Script to fetch phenotype data from OpenSNP
Mike Tung
"""
import argparse
import json
import re
import sys
import time
import urllib2

def get_profile_id(url):
    """Function to fetch IDs"""
    html = req = ''
    profile_ids = []
    flag = 1
    while 1:
        if flag == 1:
            flag = 0
            req = urllib2.urlopen(url)
            time.sleep(0.5)
            for line in req:
                line = line.lower()
                if re.search(r'<td><a href="/users/\d+".*>(.*)<', line):
                    match = re.search(r'(\d+)', line)
                    try:
                        match = match.group(1)
                        profile_ids.append(match)
                    except AttributeError:
                        pass
                elif re.search(r'<div class="pagination">', line):
                    match = re.search(r'<li class="next next_page "><a rel="next" href="(.+)"', line)
                    try:
                        match = match.group(1)
                        url = re.sub(r"\/users.*", match, url)
                        flag = 1
                    except AttributeError as e:
                        pass
        else:
                print "Done!"
                break

    return profile_ids


def parse_profile(req):
    """Function that takes a user page req obj and returns a 2d dict of  id:[phenotype:value]"""
    profile_data = {}
    key = ''
    value = ''
    for line in req:
        line = line.lower().strip()
        if re.search(r'<tr>', line):
            line = req.next()
            if re.search(r'<td><a href="/phenotypes.*>(.+)</a>', line):
                key = re.search(r'<td><a href="/phenotypes.*>(.+)</a>', line)
                key = key.group(1)
                line = req.next()
                if re.search(r'<td>(.+)</td>', line):
                    value = re.search(r'<td>(.+)</td>', line)
                    value = value.group(1)
        elif re.search(r'<p>', line):
            key = 'empty profile'
            value = 'this user has not entered any phenotypes yet'
        if key != '' and value != '':
            profile_data[key] = value
    return profile_data

def main(args):
    """Main Function to run script"""
    if args.outfile:
        #take the base url and get all the user Ids
        base_url = 'https://opensnp.org/users?direction=asc&sort=id'
        # profiles = get_profile_id(base_url)
        profiles = ['1', '2', '6', '8', '9', '10', '11', '13', '14', '15']

        #using the list of user ids makes requests to scrape their profiel
        base_url = 'https://opensnp.org/users/'
        new_url = ''
        open_snp_d = {}

        #generate snp dict
        for user in profiles:
            new_url = base_url + user
            req = urllib2.urlopen(new_url)
            print 'processing user id {0}'.format(user)
            time.sleep(0.5)
            open_snp_d[user] = parse_profile(req)

        #output json
        with open(args.outfile, 'w') as outfile:
            json.dump(open_snp_d, outfile, indent = 4)

    #Kill if req args missing
    else:
        print "Error Missing Args!"
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outfile', \
                                        metavar = '', help = 'outfile name')
    args = parser.parse_args()

    main(args)