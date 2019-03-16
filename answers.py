###################
#   fastAnswers   #
#   by @kernoeb   #
###################

# Libraries
import wikipedia
from lxml import html
import requests, html2text
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from googletrans import Translator

# Selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


def a_deepl(txt_arg):
    options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium-browser"
    browser = webdriver.Chrome(chrome_options=options)
    
    browser.get('https://www.deepl.com/translator')

    menu = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[1]/div[1]/div/button")
    menu.click()
    lang = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/button[4]")
    lang.click()
    text = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/textarea")
    text.send_keys(txt_arg)

    wait = WebDriverWait(browser, 2)
    ok = wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/p[1]"))) 
    browser.execute_script('document.evaluate("/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/p[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.style.display = "block";', ok)    
    answer = browser.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/p[1]")
    return answer.text


def a_lorem_ipsum(nb = "1"):
    url = "https://lipsum.com/feed/html?amount={}&what=paras&start=yes&generate=Generate+Lorem+Ipsum".format(nb)
    page = requests.get(url)
    c = BeautifulSoup(page.content, "html.parser")
    id = c.find("div", attrs={"id":"lipsum"})
    lorem_txt = id.text.strip()
    return lorem_txt

def a_lorem_ipsum_lang(lang = "fr"):
    url = "https://lipsum.com/feed/html?amount=1&what=paras&start=yes&generate=Generate+Lorem+Ipsum"
    page = requests.get(url)
    c = BeautifulSoup(page.content, "html.parser")
    id = c.find("div", attrs={"id":"lipsum"})
    lorem_txt = id.text.strip()

    t = Translator().translate(lorem_txt, src='la', dest=lang).text
    return t 

def a_meteo(loc):
    geolocator = Nominatim()
    location = geolocator.geocode(loc)
    lat = location.latitude
    lon = location.longitude

    url = "https://weather.com/fr-FR/temps/aujour/l/{},{}".format(lat, lon)
    try:
        page = requests.get(url)
        c = BeautifulSoup(page.content, "html.parser")
        id = c.find("div", attrs={"class":"today_nowcard-temp"})
        ret = id.text.strip()
    except:
        ret = "Erreur : Site weather.com en panne ou en maintenance. Si le problème perdure, veuillez contacter @kernoeb"
    return ret


def a_cntrl(mot):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    url = "http://www.cnrtl.fr/lexicographie/{}".format(mot)
    try:
        page = requests.get(url)
        c = BeautifulSoup(page.content, "html.parser")
        id = c.find("div", attrs={"id":"lexicontent"})
        ret = h.handle(str(id))
    except:
        ret = "Erreur : Site CNTRL.COM en panne."
    return ret


def a_wikipedia(recherche, lang = "fr"):
    wikipedia.set_lang(lang)
    try:
        page = wikipedia.page(recherche)
        answer = str(page.summary) + "\n\n" + str(page.url)
    except:
        answer = "Cet article n'existe pas..."    

    return answer

# print(a_deepl("Pomme de terre"))
# print(a_lorem_ipsum())
# print(a_lorem_ipsum_lang())
# print(a_meteo("Paris"))
# print(a_cntrl("chat"))
# print(a_wikipedia("Google"))
