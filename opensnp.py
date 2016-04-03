#!/usr/bin/env python
"""
A Script to Download All User Profiles from Opensnp.org
Mike Tung
"""
import json
import re
import sys
import time
import urllib2

def get_ids():
    """A Function to fetch all opensnp IDs and return them as a list"""
    url = 'https://opensnp.org/users?direction=asc&page=1&sort=id'
    html = req = ''
    profile_ids = []
    flag = 1
    #process the webpage and if there is a next webpage, go there and repeat
    while 1:
        if flag == 1:
            flag = 0
            req = urllib2.urlopen(url)
            time.sleep(0.3)
            print "Processing ids"
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

def process_ids(profiles):
    """A function to process each opensnp profile given a list of ids"""
    base_url = 'https://opensnp.org/users/'
    new_url = ''
    user_dict = {}
    user_profile_dict = {}

    #For each user id go through their profile and extract the phenotype and value
    #store as a dictionary that is then incorporated into a bigger dictionary.
    for user in profiles:
        new_url = base_url + user
        req = urllib2.urlopen(new_url)
        time.sleep(0.3)
        key = value = ''
        for line in req:
            line = line.lower()
            if re.search(r'<td><a href="/phenotypes/\d*">(.*)<', line):
                key = re.search(r'<td><a href="/phenotypes/\d*">(.*)</a></td>', line).group(1)
                line = req.next().lower()
                if re.search(r'<td>(.*)</td>', line):
                    value = re.search(r'<td>(.*)</td>', line).group(1)
                    key, value = clean_html(key, value)
                    user_profile_dict[key] = value
            elif re.search(r'<p>this user has not entered any phenotypes yet.</p>', line):
                user_profile_dict['profile'] = 'empty'
        user_dict[user] = user_profile_dict
    return user_dict

def clean_html(key, value):
    key = key.replace('&#x27;', "'")
    key = key.replace('&#39;', "'")
    key = key.replace('&quot;', '"')
    key = key.replace('&amp;', '&')
    key = key.replace('( ', '(')
    key = key.replace(' )', ')')
    key = key.replace('[ ', '[')
    key = key.replace(' ]', ']')
    key = key.replace('>&bull;&nbsp;', '')
    key = key.replace('\xe2\x80\x94' , '---')

    value = value.replace('&#x27;', "'")
    value = value.replace('&#39;', "'")
    value = value.replace('&quot;', '"')
    value = value.replace('&amp;', '&')
    value = value.replace('( ', '(')
    value = value.replace(' )', ')')
    value = value.replace('[ ', '[')
    value = value.replace(' ]', ']')
    value = value.replace('>&bull;&nbsp;', '')
    value = value.replace('\xe2\x80\x94' , '---')

    return (key, value)


def main():
    """Main Function to Run Everything"""
    #get my ids
    id_li = get_ids()

    #from list of ids process the profiles and return master 2d Dict
    open_snp_d = process_ids(id_li)

    #output master dict as json file.
    with open('opensnp_data.json', 'w') as outfile:
        json.dump(open_snp_d, outfile, sort_keys = True, indent = 4)

#if running script as standalone then execute main function.
if __name__ == '__main__':
    main()