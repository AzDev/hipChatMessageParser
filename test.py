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
import concurrent.futures

class hipChatMessageParser(object):
    """
    >>> hipTest_1 = hipChatMessageParser('@chris; you around? <a href="http://www.google.com">google site</a>', False)
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
    >>> hipTest_1 = hipChatMessageParser('Good morning! (coffee) () (4ai) (un:own) (itwillben0tparsed)')
    >>> hipTest_1.get_emoticons
    ['coffee', '4ai']
    >>> hipTest_1 = hipChatMessageParser('@chris you around?')
    >>> hipTest_1.to_json()
    {'mentions': ['chris']}
    >>> hip_parsed_2 = hipChatMessageParser('Good morning! (megusta) (coffee)')
    >>> hip_parsed_2.to_json()
    {'emoticons': ['megusta', 'coffee']}
    >>> hip_parsed_3 = hipChatMessageParser('Olympics are starting soon; <a href="http://www.nbcolympics.com/" target="_blank"><b><span style="color:red;text-decoration:none">MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be</span></b><span style="color:#3572b0;text-decoration:none"> http://www.nbcolympics.com"</span></a>')
    >>> hip_parsed_3.to_json()
    {'links': [{'url': '<a href="http://www.nbcolympics.com/" target="_blank"><b><span style="color:red;text-decoration:none">MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be</span></b><span style="color:#3572b0;text-decoration:none"> http://www.nbcolympics.com"</span></a>', 'title': 'NBC Olympics | Home of the 2016 Olympic Games in Rio'}]}
    >>> hip_parsed_4 = hipChatMessageParser('@bob @john (success) such a cool feature; <a href="https://twitter.com/jdorfman/status/430511497475670016" target="_blank"><span style="color:#3572b0;text-decoration:none">https://twitter.com/<wbr>jdorfman/status/<wbr>430511497475670016"</span></a>')
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

# you can use this function if you need only print output  
def multithread_json_printer(hip_chat_message):
    hip_parsed = hipChatMessageParser(hip_chat_message)
    print "input is:", hip_chat_message
    print "JSON output is:", hip_parsed.to_json()
    print ""

# u can operate result of parsing in the body of this function
# if u need to do smth with it using multithreading
def multithread_json_parser(hip_chat_message):
    hip_parsed = hipChatMessageParser(hip_chat_message)
    print "input is:", hip_chat_message
    json_str = hip_parsed.to_json()
    #N! do smth with json_str.....
    #N!
    #N! or return as a result to shared list:
    # return hip_parsed.to_json()

if __name__ == "__main__":
    hipChat_messages = ['@chris you around?', 'Good morning! (megusta) (coffee)']

    # returns in the order given
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(multithread_json_printer, hipChat_messages)
