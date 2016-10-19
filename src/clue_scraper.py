import urllib3
from bs4 import BeautifulSoup

BASE_SEARCH_URL = 'http://www.wordplays.com/crossword-solver/'

def get_clue_possible_answers(clue, target_length):
    """
    returns an array of strings with length target_lengths retrieved from 
    scraping the Internet for possible answers to clue, or None if there is
    an error
    """
    http = urllib3.PoolManager()
    response = http.request('GET', BASE_SEARCH_URL + clue)
        
    if response.status != 200:
        return None
    
    soup = BeautifulSoup(response.data, "lxml")
    cluelist = soup.find(id="wordlists")
    
    if cluelist == None:
        return None
    
    clue_labels = cluelist.findAll("td", { "class" : "clue" })
    possibilities = []
    for label in clue_labels:
        prev_sib = label.previous_sibling
        if prev_sib == None:
            continue
        link = prev_sib.a
        if link == None:
            continue
        link_name = link.contents[0]
        if link == None:
            continue
        clue = str(link_name);
        if len(clue) == target_length:
            print("adding:" + clue)
            possibilities.append(clue)
            
    return possibilities