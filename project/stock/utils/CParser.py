from HTMLParser import HTMLParser

class CParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.codeflag = False
        self.msgflag = False
        self.dict = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'code':
            self.codeflag = True
        if tag == 'msg':
            self.msgflag = True

    def handle_endtag(self,tag):
        if tag == 'code':
            self.codeflag = False
        if tag == 'msg':
            self.msgflag = False

    def handle_data(self,data):
        if self.codeflag:
            self.dict['code'] = data
        if self.msgflag:
            self.dict['msg'] = data
