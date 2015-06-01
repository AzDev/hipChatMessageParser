#!N
#!N  Hip Chat message parser
#!N
#!N
#!N
#!N
#!N
#!N
#!N

import re
import urllib2

class hipChatMessageParser(object):

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
                return self._find_in_string(rtf_url[0], r'<a.*?=".*?"')[0].split('"')[1]
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



# Sample 1:
hip_parsed_1 = hipChatMessageParser('@chris you around?')
print "input is:", "@chris you around?"
print "JSON output is:", hip_parsed_1.to_json()
print ""
# Sample 2:
hip_parsed_2 = hipChatMessageParser('Good morning! (megusta) (coffee)')
print "input is:", "Good morning! (megusta) (coffee)"
print "JSON output is:", hip_parsed_2.to_json()
print ""
# Sample 3:
# In third and forth example there are a links with a lot of tags so they were get as is
hip_parsed_3 = hipChatMessageParser('Olympics are starting soon; <a href="http://www.nbcolympics.com/" target="_blank"><b><span style="color:red;text-decoration:none">MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be</span></b><span style="color:#3572b0;text-decoration:none"> http://www.nbcolympics.com"</span></a>')
print "input is:", 'Olympics are starting soon; <a href="http://www.nbcolympics.com/" target="_blank"><b><span style="color:red;text-decoration:none">MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be</span></b><span style="color:#3572b0;text-decoration:none"> http://www.nbcolympics.com"</span></a>'
print "JSON output is:", hip_parsed_3.to_json()
print ""
# Sample 4:
hip_parsed_4 = hipChatMessageParser('@bob @john (success) such a cool feature; <a href="https://twitter.com/jdorfman/status/430511497475670016" target="_blank"><span style="color:#3572b0;text-decoration:none">https://twitter.com/<wbr>jdorfman/status/<wbr>430511497475670016"</span></a>')
print "input is:", '@bob @john (success) such a cool feature; <a href="https://twitter.com/jdorfman/status/430511497475670016" target="_blank"><span style="color:#3572b0;text-decoration:none">https://twitter.com/<wbr>jdorfman/status/<wbr>430511497475670016"</span></a>'
print "JSON output is:", hip_parsed_4.to_json()
print ""
