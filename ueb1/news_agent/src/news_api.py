import requests
from bs4 import BeautifulSoup


class NewsAPI:    
    def get_news_categories(self):  
        raw_html = requests.get("https://www.tagesschau.de").text
        html = BeautifulSoup(raw_html, "html.parser")

        categories = html.find(class_ = "horizontal-nav horizontal-nav--swipenav").findChildren("ul", recursive=False)
        categories = categories[0].find_all("a")
        
        news_categories = {}
        for category in categories:
            news_categories[category.get_text()] = category.get("href")
        
        return news_categories

    def get_category_news(self, link):
        raw_html = requests.get(link).text
        html = BeautifulSoup(raw_html, "html.parser")
        
        article_list = {}
        
        teasers = html.find_all("a", {"class": "teaser__link"})
        for teaser in teasers:
            article_link = teaser.get("href")
            topline = teaser.find_all("span", {"class": "teaser__topline"})[0].get_text()
            headline = teaser.find_all("span", {"class": "teaser__headline"})[0].get_text()
            
            if article_link is None or article_link == "":
                continue
            
            if topline is None or topline == "":
                continue
            
            if headline is None or headline == "":
                continue

            article_list[article_link] = [topline, headline]
        
        return article_list

    def get_article_text(self, link):
        raw_html = requests.get(link).text
        html = BeautifulSoup(raw_html, "html.parser")
        
        text = ""
        paragraphs = html.find_all("p", {"class": "textabsatz"})
        for p in paragraphs:
            text += p.get_text()
        
        return text

