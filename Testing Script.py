from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://pricebaba.com/tablet/brands'
r = requests.get(url)
s = BeautifulSoup(r.content, 'html.parser')

tablet = s.find_all('a',{'class':'txt-al-c'})
tablet = [pt['href'] for pt in tablet]
tablet_url = []

for i in tablet:
    urls = str("https://pricebaba.com") + str(i)
    tablet_url.append(urls)

tablet_details = []

for i in tablet_url:
    r = requests.get(i)
    s = BeautifulSoup(r.content, 'html.parser')

    tablet = s.find_all('span',{'class':'productSKULink target_link'})
    tablet = [pt['data-href'] for pt in tablet]
    
    tablet_details.append(tablet)
    
tablet_details = [item for sublist in tablet_details for item in sublist]

tablet_details = list(dict.fromkeys(tablet_details))
tablet_details = tablet_details[:20]
Tablet = pd.DataFrame()

for i in tablet_details:
    
    r = requests.get(i)
    s = BeautifulSoup(r.content, 'html.parser')
    
    ModelName = s.find_all('h1',{'class':'txt-wt-b txt-xl'})
    ModelName = [pt.get_text().strip() for pt in ModelName]
    
    Price = s.find_all('div',{'class':'txt-xl txt-wt-b txt-clr-light-black lowestPrice pb-tbl-center--ends'})
    Price = [pt.get_text().strip() for pt in Price]
    
    Ratings = s.find_all('div',{'class':'m-v-xs txt-clr-grey txt-underline p-l-s'})
    Ratings = [pt.get_text().replace("\xa0"," ").split(" & ")[0].replace(" Ratings","").replace(",",'') for pt in Ratings]

    Stars = s.find('div',{'class':'cui-rating'})
    
    Image = s.find_all('div',{'class':'gllry__itm--tbl-cll'})
    try:
        Image = Image[0].find_all('img')
        Image = [pt['data-src'] for pt in Image]
    except:
        Image = []

    try:
        Stars = [pt.get_text() for pt in Stars]
    except:
        Stars = []
    
    specification = s.find_all('ul',{'class':'quick-spec ul-list'})
   
    try:
        list_specification = [pt.find_all('span') for pt in specification[0]]
    except:
        list_specification = []
        
    list_specification = [item for sublist in list_specification for item in sublist]
    list_specification = [pt.get_text().strip() for pt in list_specification]

    Screen = []
    RAM = []
    ROM = []
    Battery = []

    for text in list_specification:
        if 'Screen' in text:
            Screen.append(text)
        elif 'RAM' in text:
            RAM.append(text)
        elif 'Storage' in text:
            ROM.append(text)
        elif 'mAh' in text:
            Battery.append(text)
        else:
            pass
    
    Specification = [", ".join(list_specification)]
    
    TabletDetails = pd.DataFrame({
        "Tablet Name": pd.Series(ModelName),
        "RAM GB": pd.Series(RAM),
        "ROM GB": pd.Series(ROM),
        "Screen": pd.Series(Screen),
        "Battery": pd.Series(Battery),
        "Specification": pd.Series(Specification),
        "Price": pd.Series(Price),
        "Image": pd.Series(Image),
        "Link": pd.Series([i])
        })
    
    Tablet = Tablet.append(TabletDetails,ignore_index=True)