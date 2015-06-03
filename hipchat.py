# hipchat - Module with the hipChat functionality
# It is the demo version and only message parser is available
#
# Copyright (c) 2015 by Elman Liutfaliiev <elman.liutfaliiev@gmail.com>

r"""
This module is a solution that takes a chat message string and returns a JSON
string containing information about its contents. Special content to look for
includes:
1. @mentions - A way to mention a user. Always starts with an '@' and ends when
   hitting a non-word character.
  (http://help.hipchat.com/knowledgebase/articles/64429-how-do-mentions-work-)
2. Emoticons - For this exercise, you only need to consider 'custom' emoticons
   which are alphanumeric strings, no longer than 15 characters, contained in
   parenthesis. You can assume that anything matching this format is an emoticon.
   (https://www.hipchat.com/emoticons)
3. Links - Any URLs contained in the message, along with the page's title.
 
For example, calling your function with the following inputs should result in the
corresponding return values.

Input: "@chris you around?"
Return (string):
{
  "mentions": [
    "chris"
  ]
}
 
Input: "Good morning! (megusta) (coffee)"
Return (string):
{
  "emoticons": [
    "megusta",
    "coffee"
  ]
}
 
Input: "Olympics are starting soon; MailScanner has detected a possible fraud
attempt from "www.nbcolympics.com" claiming to be http://www.nbcolympics.com"
Return (string):
{
  "links": [
    {
      "url": "MailScanner has detected a possible fraud attempt from
"www.nbcolympics.com" claiming to be http://www.nbcolympics.com",
      "title": "NBC Olympics | 2014 NBC Olympics in Sochi Russia"
    }
  ]
}
 
Input: "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016"
Return (string):
{
  "mentions": [
    "bob",
    "john"
  ],
  "emoticons": [
    "success"
  ],
  "links": [
    {
      "url": "https://twitter.com/jdorfman/status/430511497475670016",
      "title": "Twitter / jdorfman: nice @littlebigdetail from ..."
    }
  ]
}

Information about how this module can be used can be found below.
Using the hipchat module
===========================
This module defines one class called MessageParser:
class MessageParser(string, autoparsing=True):
Arguments are:
string should be a string and it is a string which will be parsed.
autoparsing=True (default): In this case, the string will be parsed immediately.

This module also defines some shortcut functions:
to_json(cmd):
    Return parsed string in a JSON format.
   
"""

import re
import urllib2

class MessageParser(object):
    """
    >>> hipTest_1 = MessageParser('@chris; you around? <a href="http://www.google.com">google site</a>', False)
    >>> hipTest_1.get_mentions
    ['chris']
    >>> hipTest_1.get_rtf_url
    ['<a href="http://www.google.com">google site</a>']
    >>> hipTest_1.get_url
    'http://www.google.com'
    >>> hipTest_1.get_title('http://www.google.com')
    'Google'
    >>> hipTest_1.get_title('ww.g.om')
    'unable to read title'
    >>> hipTest_1.get_links
    [{'url': '<a href="http://www.google.com">google site</a>', 'title': 'Google'}]
    >>> hipTest_1.string = "<a hef=>gogle"
    >>> hipTest_1.get_links
    >>> hipTest_1 = MessageParser('Good morning! (coffee) () (4ai) (un:own) (itwillben0tparsed)')
    >>> hipTest_1.get_emoticons
    ['coffee', '4ai']
    >>> hipTest_1 = MessageParser('@chris you around?')
    >>> hipTest_1.to_json()
    {'mentions': ['chris']}
    >>> hip_parsed_2 = MessageParser('Good morning! (megusta) (coffee)')
    >>> hip_parsed_2.to_json()
    {'emoticons': ['megusta', 'coffee']}
    >>> hip_parsed_3 = MessageParser('Olympics are starting soon; <a href="http://www.nbcolympics.com/" target="_blank"><b><span style="color:red;text-decoration:none">MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be</span></b><span style="color:#3572b0;text-decoration:none"> http://www.nbcolympics.com"</span></a>')
    >>> hip_parsed_3.to_json()
    {'links': [{'url': '<a href="http://www.nbcolympics.com/" target="_blank"><b><span style="color:red;text-decoration:none">MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be</span></b><span style="color:#3572b0;text-decoration:none"> http://www.nbcolympics.com"</span></a>', 'title': 'NBC Olympics | Home of the 2016 Olympic Games in Rio'}]}
    >>> hip_parsed_4 = MessageParser('@bob @john (success) such a cool feature; <a href="https://twitter.com/jdorfman/status/430511497475670016" target="_blank"><span style="color:#3572b0;text-decoration:none">https://twitter.com/<wbr>jdorfman/status/<wbr>430511497475670016"</span></a>')
    >>> hip_parsed_4.to_json()
    {'mentions': ['bob', 'john'], 'emoticons': ['success'], 'links': [{'url': '<a href="https://twitter.com/jdorfman/status/430511497475670016" target="_blank"><span style="color:#3572b0;text-decoration:none">https://twitter.com/<wbr>jdorfman/status/<wbr>430511497475670016"</span></a>', 'title': 'Justin Dorfman on Twitter: &quot;nice @littlebigdetail from @HipChat (shows hex colors when pasted in chat). http://t.co/7cI6Gjy5pq&quot;'}]}
    """

    def __init__(self, string, autoparsing=True):
        self.string = string
        if autoparsing:
            self.parce_message()
        
    def parce_message(self):
    # we have to cut firstly link if exists then mentions if exists, to avoid duplicates
    # the limitation is email-adress like elman@gmail.com which can be identified like mention "@gmail"
        self.links = self.get_links
        self.cut_links
        self.mentions = self.get_mentions
        self.cut_mentions
        self.emoticons = self.get_emoticons

    def to_json(self):
        result_dict = {}
        if self.mentions:
            result_dict["mentions"] = self.mentions
        if self.emoticons:
            result_dict["emoticons"] = self.emoticons
        if self.links:
            result_dict["links"] = self.links
        return result_dict

    @property
    def get_mentions(self):
        return [item[1:] for item in self._find_in_string(self.string, r'@\w+')]

    @property
    def cut_mentions(self):
        self.string = self._cut_from_string(self.string, r'@\w+')

    @property
    def get_emoticons(self):
        return [item[1:-1] for item in self._find_in_string(self.string, r'\(\w{1,15}\)')]

    @property
    def cut_emoticons(self):
        self.string = self._cut_from_string(self.string, r'\(\w{1,15}\)')

    @property
    def cut_links(self):
        self.string = self._cut_from_string(self.string, r'<a.*\/a>')

    @property
    def get_url(self):
        rtf_url = self.get_rtf_url
        if rtf_url:
            try:
                tagged_url = self._find_in_string(rtf_url[0], r'<a.*?=".*?"')[0]
                url = tagged_url.split('"')[1]
                return url
            except:
                return 'url is broken'

    @property
    def get_rtf_url(self):
        return self._find_in_string(self.string, r'<a.*\/a>')

    def get_title(self, url):
        try:
            sock = urllib2.urlopen(url)
            htmlSource = sock.read()
            sock.close()
            title_tag = self._find_in_string(htmlSource, r'<title.*title>')
            return self._find_in_string(title_tag[0], r'>.*<')[0][1:-1]
        except:
            return 'unable to read title'
            
    @property
    def get_links(self):
        url = self.get_rtf_url
        if url:
            title = self.get_title(self.get_url)
            return [{"url": url[0], "title": title}]
        else:
            return None

    def _find_in_string(self, string, search_mask):
        return re.findall(search_mask, string)

    def _cut_from_string(self, string, search_mask):
        p = re.compile(search_mask)
        result_str = p.subn('', string)[0]
        return result_str
