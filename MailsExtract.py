from googlesearch import search
import re
import urllib.request
import ssl
import time
from email_validator import validate_email, EmailNotValidError


class Extractor:

    def __init__(self, target):
        self.target = target

    def googlesearch(self):
        query = "intext:@"+self.target
        urls = []
        for j in search(query, tld="co.in", num=3, stop=3, pause=2):
            urls.append(j)
        print(urls)
        return urls

    @staticmethod
    def request(url):
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib.request.urlopen(url)
        html = req.read()
        return html

    @staticmethod
    def replace(data):
        data = data.decode('ISO-8859-1')
        data = data.replace(" [at] ", "@")
        data = data.replace(" &agrave ", "@")
        data = data.replace("at", "@")
        return data

    @staticmethod
    def process(data):
        emails = []
        regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_'{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_'" 
                            "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                            "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
        #for email in re.findall(r'[a-zA-Z0-9.\-_+#~!$&\',;=:]+'+ '@' + r'[a-zA-Z0-9.-]*', data):
        for email in re.findall(regex, data):
            emails.append(email)
        return emails

    @staticmethod
    def checkmails(emails):
        valid = []
        for email in emails:
            try:
                v = validate_email(email)  # validate and get info
                email = v["email"]  # replace with normalized form
                valid.append(email)
            except EmailNotValidError as e:
                pass
        return valid

    def crawl(self):
        emails = []
        urls = self.googlesearch()
        for url in urls:
            time.sleep(10)
            data = self.request(url)
            data = self.replace(data)
            email = self.process(data)
            emails.extend(email)
            #emails = self.checkmails(emails)
        return emails


if __name__ == '__main__':
    e = Extractor("mi.parisdescartes.fr")
    print(e.crawl())

