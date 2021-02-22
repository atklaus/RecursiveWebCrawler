from urllib.request import urlopen
from html.parser import HTMLParser
parser = HTMLParser()
from urllib.request import urlopen, Request
import re
from urllib.parse import urljoin
import time

#List of stop words
STOP_WORDS = ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again',
'against', 'all', 'almost', 'alone', 'along', 'already', 'also',
'although', 'always', 'am', 'among', 'amongst', 'amoungst',
'amount', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone',
'anything', 'anyway', 'anywhere', 'are', 'area', 'areas', 'around',
'as', 'ask', 'asking', 'asked', 'asks', 'at', 'b', 'back', 'backed',
'backing', 'backs' 'be','became', 'because', 'become', 'becomes',
'becoming', 'been', 'before', 'began', 'beforehand', 'behind', 'being',
'beings', 'best', 'better', 'below', 'beside', 'besides',
'between', 'beyond', 'big', 'bill', 'both', 'bottom', 'but', 'by', 'c',
'call', 'came', 'can', 'cannot', 'cant', 'case', 'cases', 'certain',
'certainly', 'clear', 'clearly', 'come', 'computer', 'con', 'could',
'couldnt', 'cry', 'd', 'de', 'describe', 'detail', 'did', 'differ',
'different', 'differently', 'do', 'does', 'done', 'down', 'downed',
'downing', 'downs', 'dr', 'due', 'during', 'e', 'each', 'early', 'eg',
'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'end', 'ended',
'ending', 'ends', 'enough', 'etc', 'even', 'evenly', 'ever', 'every',
'everybody', 'everyone', 'everything', 'everywhere', 'except', 'f', 'face',
'faces', 'fact', 'facts', 'far', 'felt', 'few', 'fifteen', 'fifty', 'fill',
'find', 'finds', 'fire', 'first', 'five', 'for', 'former', 'formerly',
'forty', 'found', 'four', 'from', 'front', 'full', 'fully', 'further',
'furthered', 'furthering', 'furthers', 'g', 'gave', 'general', 'generally',
'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods',
'got', 'great', 'greater', 'greatest', 'group', 'grouped', 'groups', 'had',
'h', 'had', 'has', 'hasnt', 'have', 'having', 'he', 'hence', 'her',
'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself',
'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however',
'hundred', 'i', 'ie', 'if', 'important', 'in', 'inc', 'indeed',
'interest', 'interested', 'interesting', 'interests', 'into', 'is',
'it', 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kind',
'knew', 'know', 'known', 'knows', 'l', 'large', 'largely', 'last',
'later', 'latest', 'latter', 'latterly', 'least', 'less', 'let',
'lets', 'like', 'likely', 'long', 'longer', 'longest', 'ltd', 'm', 'made',
'make', 'making', 'man', 'many', 'may', 'me', 'meanwhile', 'member',
'members', 'men', 'might', 'mill', 'mine', 'more', 'moreover',
'most', 'mostly', 'move', 'mr', 'mrs', 'ms', 'much', 'must', 'my',
'myself', 'n', 'name', 'namely', 'necessary', 'need', 'needed', 'needing',
'needs', 'neither', 'never', 'nevertheless', 'new', 'newer', 'newest',
'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor', 'not',
'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off',
'often', 'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'onto',
'open', 'opened', 'opening', 'opens', 'or', 'order', 'ordered', 'ordering',
'orders', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
'over', 'own', 'p', 'part', 'parted', 'parting', 'parts', 'per', 'perhaps',
'place', 'places', 'please', 'point', 'pointed', 'pointing', 'points',
'possible', 'present', 'presented', 'presenting', 'presents', 'problem',
'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 're', 'really',
'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says',
'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees',
'serious', 'several', 'shall', 'she', 'should','show', 'showed', 'showing',
'shows', 'side', 'sides', 'since', 'sincere', 'six', 'sixty', 'small',
'smaller', 'smallest', 'so', 'some', 'somebody', 'somehow', 'someone',
'something', 'sometime', 'sometimes', 'somewhere', 'state', 'states', 'still',
'such', 'sure', 'system', 't', 'take', 'taken', 'ten', 'than',
'that', 'the', 'their', 'them', 'themselves', 'then', 'thence',
'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon',
'these', 'they', 'thick', 'thin', 'thing', 'things', 'think', 'thinks',
'third', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through',
'throughout', 'thru', 'thus', 'to', 'today', 'together', 'too', 'took', 'top',
'toward', 'towards', 'turn', 'turned', 'turning', 'turns', 'twelve', 'twenty',
'two', 'u', 'un', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses',
'v', 'very', 'via', 'w', 'want', 'wanted', 'wanting', 'wants', 'was', 'way',
'ways', 'we', 'well', 'wells', 'went', 'were', 'what', 'whatever', 'when',
'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein',
'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who',
'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within',
'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year',
'years', 'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours',
'yourself', 'yourselves', 'z']


class Collector(HTMLParser):

    """
    Extends the htmlparser to be used for custom web scraping

    Attributes
    ----------
    word_list : list 
        list of words from a given url
    url : str
        url string to search
    links: list
        links found on web page
    """

    def __init__(self, url):
        'initializes the parser'
        HTMLParser.__init__(self)
        self.word_list = []
        self.url = url
        self.links = []

    def handle_starttag(self, tag, attrs):
                
        """
        print value of href attribute if any

        Parameters
        ----------
        tag : str 
            html tag to parse
        attrs: list
            values from a given tag
        """
        
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    # construct absolute URL
                    absolute = urljoin(self.url, attr[1])
                    if absolute[:4] == 'http' and self.url in absolute: # collect HTTP URLs
                        self.links.append(absolute)
        

    def handle_data(self, data):
        """
        get text not in tags from url

        Parameters
        ----------
        data : str  
            line by line text data from website
        """

        words = data.split()
        for word in words: #iterate through each word in a line
            word = re.sub(r'[^\w\s]', '', word)  #regex to remove all punctuation from words
            if (word not in STOP_WORDS) and (not word.isnumeric()) and (len(word)>1): #checks of words to include
                self.word_list = self.word_list + [word] #append word to word_list

    def getData(self):
        """
        get the word_list
        """
        return self.word_list

    def getLinks(self):
        """
        get unique links
        """
        return list(set(self.links))


class WebCrawl:
    """
    Sequence methods to crawl and entire website

    Attributes
    ----------
    url : str 
        base url to parse
    visited : set
        set of all pages visited
    freq: dict
        dictionary of words of entire website
    """

    def __init__(self, url):
        """
        instantiate webcrawl with these values
        """
        self.url = url
        self.visited = set() # initialize visited to an empty set
        self.set_headers() #set the headers to be used in the request
        self.freq = {}

    def crawl(self, url):
        '''
        a recursive web crawler that calls analyze()
        on every visited web page

        Parameters
        ----------
        url : str 
            current url to be called
        '''

        self.visited.add(url) #add url to pages visited

        # analyze() returns a list of hyperlink URLs in web page url 
        links = self.analyze(url)

        # recursively continue crawl from every link in links
        for link in links:
            # follow link only if not visited
            if link not in self.visited:
                try:
                    self.crawl(link)
                except:
                    pass

    def set_headers(self):
        """
        define the headers used in requesting the request

        Attributes
        ----------
        header : str 
            description of the ip address, browser configuration where the request is coming from
        """
        userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36'
        headers = {'User-Agent': userAgent}
        self.headers = headers

    def get_content(self, url):
        """
        get the content from a given url

        Parameters
        ----------
        url : str 
            web address for current page being scraped
        """

        collector = Collector(url)
        request = Request(url,headers=self.headers)

        with urlopen(request) as response: #use context manager to run the request with specified headers
            content = response.read()
            content = content.decode().lower()
            content = re.sub(r'<script.+?</script>', '', content, flags=re.DOTALL) #removes all javascript from text
            content = re.sub(r'<style.+?</style>', '', content, flags=re.DOTALL) #removes all css from text
            collector.feed(content) # passes text from website

        self.collector = collector

    def analyze(self, url):
        """
        get the content from a given url

        Parameters
        ----------
        url : str 
            web address for current page being scraped

        :return links: all links on current web page 
        """

        print('\n\nVisiting', url)           # for testing

        self.get_content(url)
        word_list = self.collector.word_list #gets list of words from the instatiated collector obj
        self.frequency(word_list) #acumulate word list from this page to freq attribute
        links = self.collector.getLinks()          # get list of links

        # print the frequency of every text data word in web page
        print('\n{:45} {:10} {:5}'.format('URL', 'word', 'count'))
        for word in self.freq:
            print('{:45} {:10} {:5}'.format(url, word, self.freq[word]))

        # print the http links found in web page
        print('\n{:45} {:10}'.format('URL', 'link'))
        for link in links:
            print('{:45} {:10}'.format(url, link))
        
        return links

    def frequency(self, word_list):
        """
        passes in the list of words from a given web page and adds there counts to freq attribute

        Parameters
        ----------
        word_list : list 
            list of words scraped from website
        """

        for word in word_list:
            if word in self.freq.keys():
                self.freq[word] +=  word_list.count(word)
            else:
                self.freq[word] =  word_list.count(word)

    def print_top(self):
        """
        Determines the top 25 words in the freq dictionary
        """
        freq_dict = self.freq

        for i in range(1,26):
            v=list(freq_dict.values())
            k=list(freq_dict.keys())
            key = k[v.index(max(v))]
            print(str(i) + '. {:30} {:20}'.format(key, freq_dict[key]))
            freq_dict.pop(key, None)


url = 'https://business.depaul.edu/'

scrapeObj = WebCrawl(url)
scrapeObj.crawl(url)
scrapeObj.print_top()




