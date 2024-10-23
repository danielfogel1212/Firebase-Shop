from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

import requests

from scrapy.selector import Selector




import urllib.request
import time
from datetime import datetime

import requests
app = Flask(__name__)
   

CORS(app)


@app.route("/<path:path>")
def index(path=None):
     headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1'
}

     response = requests.get(request.url.rstrip("?")[22:], headers=headers)
     print(response.content)
     h = []
     p = []
     pt = []
     products = []
     sel = Selector(text=response.content)
     
     heads = sel.xpath("//*[@class='s-item__wrapper clearfix']")

     for head in heads:
        h=head.xpath(".//*[@class='s-item__title']/span/text()").extract_first()
        p=head.xpath(".//*[@class='s-item__price']//text()").extract_first()
        pt=head.xpath(".//*[@class='s-item__image-wrapper image-treatment']/img/@src").extract_first()
        pl = head.xpath(".//*[@class='s-item__link']/@href").extract_first()
        products.append({"head": h, "price": p, "image":pt,"link":pl})
     return jsonify(products)


@app.route("/item/<path:path>")
def index1(path=None):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1'
}


    # Construct the full URL from the path
    
   
    # Fetch the page content from Amazon
    print(request.url.rstrip("?")[27:])
    response = requests.get(request.url.rstrip("?")[27:], headers=headers)
    
    
    # Check if the request was successful
    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve data"}), response.status_code
 
    # Parse the HTML content
    sel = Selector(text=response.content)
    products = []

# Adjusted XPath selector for product containers
    heads = sel.xpath("//div[@data-asin and contains(@class, 's-result-item')]")

    for head in heads:
     try:
         # Adjusted title and link extraction
        title_element = head.xpath(".//span[contains(@class, 'a-size-medium')]/text()").get()
        link_element = head.xpath(".//a[contains(@class, 'a-link-normal')]/@href").get()
        
        # Extract image and price
        image_url = head.xpath(".//img[@class='s-image']/@src").get(default="No image")
        price = head.xpath(".//span[@class='a-price-whole']/text()").get(default="No price")

        # Log for debugging
        print(f"Title: {title_element}, Link: {link_element}, Image: {image_url}, Price: {price}")

        # Append valid products to the list
        if title_element and link_element and image_url and price:
            products.append({
                "head": title_element.strip(),
                "price": price.strip(),
                "image": image_url,
                "link": f"https://www.amazon.com{link_element}"
            })
     except Exception as e:
        print(f"Error parsing product: {e}")

# Return the results as JSON
    return jsonify(products)

# Return the results as JSON
    return jsonify(products)  
    # Update the XPath selectors to match Amazon's structure
 
        

@app.route('/api/tasks', methods=['GET'])
def tasks():

  param_value = request.args.get('id')
  print(param_value)
  products =[]
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1'
} 
  url = "https://www.ebay.com/itm/"+str(param_value)
  response = requests.get(url, headers=headers)
  sel = Selector(text=response.content)
  print(sel.xpath("//*[@class='vim x-about-this-item']//text()").extract())
  products.append({"desc":sel.xpath("//*[@class='ux-expandable-textual-display-block-inline hide']//text()").extract_first()})
  return products


if __name__ == '__main__':
    app.run(debug=True)