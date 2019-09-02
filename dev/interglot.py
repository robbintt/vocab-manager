''' Get a response from interglot.com
'''
import urllib
import re

from bs4 import BeautifulSoup
import requests

def cleanup_phrase_for_search(text):
    ''' clean up a phrase for interglot, single spaced words only

    Not sure if I will need to deal with `ij` eventually: https://en.wikipedia.org/wiki/Dutch_orthography
    I imagine that it is not used on the internet.

    This function is really just for interglot testing and not for the final version of this tool (which would use a freedict dictionary)

    Missing: 
        - edge case, e.g. punctuation that is a word delimiter that is accidentally missing whitespace: "I went to the store.The cat was brown."
        - hyphenated and apostrophe words currently drop their hyphen or apostrophe...
    '''
    # regularize whitespace
    text = ' '.join(text.split())

    # lowercase all words
    text = text.lower()

    # strip down to alphanumerics and allowed glyphs only
    allowed_glyphs = [' ', '-', '\'']
    text_alphanum_only = ''.join([l for l in text if l.isalnum() or l in allowed_glyphs])

    return text_alphanum_only

if __name__ == '__main__':
    '''
    based on: URL = 'https://www.interglot.com/dictionary/nl/en/search?q=op+het+strand&m='
    '''
    INTERGLOT_BASE_URL = 'www.interglot.com'
    INTERGLOT_URL_PATH = 'dictionary/nl/en/search'

    # stub method, remove it if it is not expanded...
    url_terms = ('https', INTERGLOT_BASE_URL, INTERGLOT_URL_PATH, '', '', '')
    URL = urllib.parse.urlunparse(url_terms)

    words = "OP HEt Strand"
    #words = "OP"

    INTERGLOT_SEARCH_QS = { 'q' : cleanup_phrase_for_search(words) }

    resp = requests.get(URL, params=INTERGLOT_SEARCH_QS)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
    else:
        # TODO enable flask logging
        #app.logging.error("Interglot response was not 200.")
        pass

    translation_contents = soup.find_all('ol', class_='defTermListHangingIndent')
    import pdb; pdb.set_trace()
    if not translation_contents:
        # TODO enable flask logging
        #app.logging.error("No available interglot translation for {}".format(words))
        pass

    translations = [re.sub(r'\n+', '\n', c.getText()) for c in translation_contents]

    with open('definition.html', 'w') as f:
        translationdump = '\n'.join(translations)
        f.write(translationdump)
        print(translationdump)
        print(repr(translationdump))
