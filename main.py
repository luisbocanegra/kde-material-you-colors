from multiprocessing.connection import wait
import requests
from requests_html import AsyncHTMLSession
import json
from color_scheme import ColorScheme


url = "http://localhost/kde-material-you-colors/"

# create an HTML Session object
session = AsyncHTMLSession()
try:
    async def get_results():
        r = await session.get(url)
        await r.html.arender(timeout=10, sleep=2)
        return r
    
    # Use the object above to connect to needed webpage
    response =  session.run(get_results)
    # Run JavaScript code on webpage
    
except requests.exceptions.RequestException as e:
    print(e)

# find element with colors object
#print(response[0].text)

colors_element = response[0].html.find("#colors_element")


if colors_element:
    # get text from element
    colors_str = colors_element[0].text

    #print(colors_str)

    # parse colors string to json
    colors_json = json.loads(colors_str)

    with open ('putput.json', 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(str(colors_json))

    print(colors_json)
    colors_light = ColorScheme(colors_json)
    colors_light.make_light_scheme()
else:
    print('Error')
