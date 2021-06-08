import string
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



def PriceStockX(Url, auswahl):
    auswahl = auswahl + 1
    size = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/button')))
    size.click()
    price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div/div/div/div[2]/ul/li[{}]/div/div[2]'.format(auswahl))))
    price = price.text.replace(" €","")
    print("StockX Preis: " + price)
    try:
        return int(price)
    except:
        price = 9999
        return price


def Klicken(Name, auswahl):
    Klicker = driver.find_element_by_partial_link_text(Name)
    Klicker.click()
    time.sleep(3)
    Url = driver.current_url
    Preis = PriceStockX(Url, auswahl)
    return Preis

def SucheKlekt(Name, auswahl):
    Url = "https://www.klekt.com/category/all#search=" + Name
    driver.get(Url)
    time.sleep(1)
    Klicker = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pod-link")))
    Klicker.click()
    time.sleep(3)
    allSizes = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[3]/div/div[3]/div/h2/p")))
    allSizes.click()
    try:
        price = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[3]/div/div[3]/div/div[2]/div/div/div[{}]/span[2]/span[2]".format(auswahl)).text
    except:
        price = "Nicht verfügbar"
    print("Klekt Preis: " + price)
    try:
        return int(price)
    except:
        price = 9999
        return price


def SucheRestock(Name, auswahl):
    Url = "https://restocks.net/de/shop/?q=" + Name
    driver.get(Url)
    spot = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "save__first__localization__button")))
    time.sleep(2)
    spot.click()
    time.sleep(3)
    Klicker = driver.find_element_by_class_name("product-item")
    Klicker.click()
    time.sleep(2)
    driver.find_element_by_class_name("cc-compliance").click()
    time.sleep(2)
    pricebox =  driver.find_element_by_class_name("select__label")
    pricebox.click()
    time.sleep(2)
    try:
        price = driver.find_element_by_xpath("/html/body/div[4]/div[1]/ul/li[{}]/span[3]/span[1]".format(auswahl)).text
        price = price.replace(".","")
        price = price.replace("€","")
    except:
        price = "Nicht verfügbar"

    print("Restocks Preis: " + price)
    try:
        return int(price)
    except:
        price = 9999
        return price

def SucheStart(UserInput):
    search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "home-search")))
    time.sleep(4)
    search.send_keys(UserInput)
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    Names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "css-nfm48z.e1inh05x0")))
    return Names

def Preisvergleich(Preise):
    if Preise[0] <= Preise[1]:
        if Preise[0] <= Preise[2]:
            if Preise[0] <= Preise[3]:
                print("StockX ist am billigsten mit ",Preise[0], "€ und liegt unter deinem Wunschpreis. Schlag zu!")
            else:
                print("StockX ist am billigsten mit ",Preise[0], "€, liegt aber über deinem Wunschpreis")
        else:
            if Preise[2] <= Preise[3]:
                print("Klekt ist am billigsten mit ",Preise[2] , "€ und liegt unter deinem Wunschpreis. Schlag zu!")
            else:
                print("Klekt ist am billigsten mit ",Preise[2], "€, liegt aber über deinem Wunschpreis")
    elif Preise[1] <= Preise[0]:
        if Preise[1] <= Preise[2]:
            if Preise[1] <= Preise[3]:
                print("Restocks ist am billigsten mit ",Preise[1] , "€ und liegt unter deinem Wunschpreis. Schlag zu!")
            else:
                print("Restocks ist am billigsten mit ",Preise[1], "€, liegt aber über deinem Wunschpreis")
        else:
            print("Klekt ist am billigsten mit " ,Preise[2] , "€ und liegt unter deinem Wunschpreis. Schlag zu!")
    else:
        print("Klekt ist am billigsten mit ",Preise[2] , "€, liegt aber über deinem Wunschpreis")


def Start(UserInput, auswahl, Wunschpreis, size):
    global driver
    global PATH
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://stockx.com/de-de")
    print(Wunschpreis)
    Names = SucheStart(UserInput)
    Name = Names[0].text
    StockxPreis = Klicken(Name, auswahl)
    RestocksPreis = SucheRestock(Name, auswahl)
    KlektPreis = SucheKlekt(Name, auswahl)
    Preise = [StockxPreis, RestocksPreis, KlektPreis, int(Wunschpreis)]
    Preisvergleich(Preise)
    sizes = [35.5, 36, 36.5, 37.5, 38, 38.5, 39, 40, 40.5, 41, 42, 42.5, 43, 44, 44.5, 45, 45.5, 46, 47, 47.5, 48]
    Daten = [Name, StockxPreis, RestocksPreis, KlektPreis, str(sizes[size])]
    return Daten
