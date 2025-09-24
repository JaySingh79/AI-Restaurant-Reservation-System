from geopy.geocoders import Nominatim
import gradio as gr


def location_identify(text):
    
    geolocator = Nominatim(user_agent="Location") # Replace "my_app" with your application name
    location = geolocator.geocode(text)
    
    return f"Address: {location.address}, Lat long: {location.latitude, location.longitude}"
    

demo = gr.Interface(
    fn=location_identify,
    inputs=["text"],
    outputs=["text"],
)



# location2 = geolocator.reverse("52.509669, 13.376294")

# if location:
#     # print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
#     print(location2.address, location2.raw)
# else:
#     print("Location not found.")
    
    
demo.launch()
# from ip2geotools.databases.noncommercial import DbIpCity

# try:
#     response = DbIpCity.get('203.110.247.72', api_key='free')
#     print(f"Country: {response.country}")
#     print(f"City: {response.city}")
#     print(f"Latitude: {response.latitude}")
#     print(f"Longitude: {response.longitude}")
# except Exception as e:
#     print(f"Error: {e}")