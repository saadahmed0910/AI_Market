import os
from dotenv import load_dotenv
from googleplaces import GooglePlaces
load_dotenv()


google_places = GooglePlaces(os.getenv("GOOGLE_API_KEY"))


location_input = input("Search will expand with radius of r = 50km. Enter a location: ")


query_result = google_places.nearby_search (location = location_input, keyword = 'Driving School', radius = 50000)

names = []
websites = []
for place in query_result.places:
    try:
        names.append(place.name)
        place.get_details()
        websites.append(place.website)
        #print(place.website)

    except Exception as e:
        print(f"An error occurred: {e}")

if query_result.has_next_page_token:
    query_result_next_page = google_places.nearby_search(location = location_input, pagetoken=query_result.next_page_token)

competing_business = dict(zip(names, websites))