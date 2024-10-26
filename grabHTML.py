from bs4 import BeautifulSoup as soup
import requests
from places_api import competing_business
from cleaning import has_price



key_word_price = {}

for name, website in competing_business.items():
    page = has_price(website)
    
    if page:
        print("Price found for",  page)

        r = requests.get(page) #fetch HTML content
        pageSoup = soup(r.content, 'html.parser') # parsing HTML Content

        body = pageSoup.body

        if body == None:
            only_relevant_text = "None"
        else:
            only_relevant_text = body.get_text(strip=True)

        #I CANT READ WITHOUT THIS, DO NOT DELETE
        print("-------------------------------------------------------------------------------------------")

        key_word_price[name] = only_relevant_text

        
    else:
        print("No Prices Found @", page)
    

#confirmation purposes only


print("********************************************************************************************************************************************************8")
print("FINAL DICTIONARY LOOKS LIKE THIS:", key_word_price)

print ("THE AMOUNT OF PRICES COLLECTED IS: ", len(key_word_price))





 

