# AI_Market
The purpose of this code is to be able to dynamically scrape competition within a 50km radius of a type of business you would like to see the prices of.

The type of data being collected is limited by the functionality of the Google Places API. 

The code works by initially using the places api to get all businesses of the type that has been mentioned (in this case, it is driving schools) and it then searches for all businesses present on google maps within a 50km radius of the location specified by the user

The next step is to access the websites individually to search for any mention of prices alongside a description with it. If something is found, the code will retrieve the url alongside the entire text on the website which is then filtered using the openAI api to extract the description and prices. The data is stored as  JSON but is also reconfigured into a DataFrame allowing for easy storage to a SQL Database (not included)





