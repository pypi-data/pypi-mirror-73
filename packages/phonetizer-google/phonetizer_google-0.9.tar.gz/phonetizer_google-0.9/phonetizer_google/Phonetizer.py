from requests_html import HTMLSession
import re

#https://translate.google.com/#view=home&op=translate&sl=en&tl=en&text=hello
#tlid-transliteration-content transliteration-content full

class Phonetizer:
    regex = re.compile('[^a-zA-Z ]')
    def __init__(self,sentence : str,language_ : str = 'en'):
        processed=Phonetizer.regex.sub('', sentence)
        self.words=processed.lower().split()
        self.language=language_
    def get_phoname(self):
        res={}
        for word in self.words:
            print(word)
            session = HTMLSession()
            url = "https://translate.google.com/#view=home&op=translate&sl="+self.language+"&tl="+self.language+"&text="+word
            r = session.get(url)
            r.html.render()
            css = ".source-input .tlid-transliteration-content"
            out=str(r.html.find(css, first=True).text)
            print(out)
            res[word]=out.split(",")
            session.close()
        return res
