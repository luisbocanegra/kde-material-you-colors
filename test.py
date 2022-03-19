import requests
import re
url = "http://localhost/kde-material-you-colors/"
#get 5831
product_id=re.findall("",url)
#r=requests.get("https://www.electrictobacconist.com/ajax/get_product_options/{}".format(product_id))
#print([x['value'] for x in r.json()['attributes'][0]['values']])
print(page)