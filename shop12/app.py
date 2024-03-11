from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import mysql.connector
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
     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}

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



@app.route('/api/tasks', methods=['GET'])
def tasks():

  param_value = request.args.get('item')
  print(param_value)
  products =[]
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
  url = "https://www.ebay.com/itm/"+str(param_value)
  response = requests.get(url, headers=headers)
  sel = Selector(text=response.content)
  print(sel.xpath("//*[@class='vim x-about-this-item']//text()").extract())
  products.append({"desc":sel.xpath("//*[@class='ux-expandable-textual-display-block-inline hide']//text()").extract_first()})
  return products


if __name__ == '__main__':
    app.run(debug=True)