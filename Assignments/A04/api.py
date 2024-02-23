# Libraries for FastAPI
from fastapi import FastAPI, Query, Path
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from pymongo import MongoClient
from typing import List
from pydantic import BaseModel
from mongoManager import MongoManager
import re

# Builtin libraries
import os

from random import shuffle

"""
           _____ _____   _____ _   _ ______ ____
     /\   |  __ \_   _| |_   _| \ | |  ____/ __ \
    /  \  | |__) || |     | | |  \| | |__ | |  | |
   / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
  / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
 /_/    \_\_|   |_____| |_____|_| \_|_|    \____/

The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
"""

description = """🤡
(new description that's not out of pocket or fbi watchlist worthy)🤡


## Description:
(Ill keep this one)
Sweet Nostalgia Candies brings you a delightful journey through time with its extensive collection of 
candies. From the vibrant, trendy flavors of today to the cherished, classic treats of yesteryear, 
our store is a haven for candy lovers of all ages (but mostly kids). Step into a world where every shelf and corner 
is adorned with jars and boxes filled with colors and tastes that evoke memories and create new ones. 
Whether you're seeking a rare, retro candy from your childhood or the latest sugary creation, Sweet 
Nostalgia Candies is your destination. Indulge in our handpicked selection and experience a sweet 
escape into the world of confectionery wonders! And don't worry! We will watch your kids!! (😉)

#### Contact Information:

- **Address:** 3410 Taft Blvd, Wichita Falls, TX 76308.
- **Phone:** (123) 968-7378 [or (123 you-perv)]
- **Email:** perv@kidsinvans.com
- **Website:** http://24.144.91.90:8084

"""

# Needed for CORS
# origins = ["*"]


# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="KidsInVans.Fun🤡",
    description=description,
    version="0.0.1",
    terms_of_service="http://www.kidsinvans.fun/worldleterms/",
    contact={
        "name": "KidsInVans.Fun",
        "url": "http://www.kidsinvans.fun/worldle/contact/",
        "email": "perv@www.kidsinvans.fun",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Needed for CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

"""
  _      ____   _____          _         _____ _                _____ _____ ______  _____
 | |    / __ \ / ____|   /\   | |       / ____| |        /\    / ____/ ____|  ____|/ ____|
 | |   | |  | | |       /  \  | |      | |    | |       /  \  | (___| (___ | |__  | (___
 | |   | |  | | |      / /\ \ | |      | |    | |      / /\ \  \___ \\___ \|  __|  \___ \
 | |___| |__| | |____ / ____ \| |____  | |____| |____ / ____ \ ____) |___) | |____ ____) |
 |______\____/ \_____/_/    \_\______|  \_____|______/_/    \_\_____/_____/|______|_____/

This is where you will add code to load all the countries and not just countries. Below is a single
instance of the class `CountryReader` that loads countries. There are 6 other continents to load or
maybe you create your own country file, which would be great. But try to implement a class that 
organizes your ability to access a countries polygon data.
"""

mm = MongoManager(db="candy_store")

"""
  _      ____   _____          _        __  __ ______ _______ _    _  ____  _____   _____
 | |    / __ \ / ____|   /\   | |      |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
 | |   | |  | | |       /  \  | |      | \  / | |__     | |  | |__| | |  | | |  | | (___
 | |   | |  | | |      / /\ \ | |      | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \
 | |___| |__| | |____ / ____ \| |____  | |  | | |____   | |  | |  | | |__| | |__| |____) |
 |______\____/ \_____/_/    \_\______| |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/

This is where methods you write to help with any routes written below should go. Unless you have 
a module written that you include with statements above.  
"""


"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/

 This is where your routes will be defined. Routes are just python functions that retrieve, save, 
 delete, and update data. How you make that happen is up to you.
"""

"""
Used for delete and two searches
"""
client = MongoClient()
database = client["candy_store"]
collection = database["candies"]


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


"1"
@app.get("/candies")
def list_all_candies():
    """
    Retrieve a list of all candies available in the store.
    """
    mm.setCollection("candies")
    result = mm.get(filter={"_id": 0})
    return result

"2"
@app.get("/categories")
def list_all_categories():
    """
    Get a list of candy categories (e.g., chocolates, gummies, hard candies).
    """
    mm.setCollection("categories")
    result = mm.get(filter={"_id": 0})
    return result

"3"
@app.get("/candies/category/{category}")
def candies_by_category(category: str):
    """
    Search for candies based on a query string (e.g., name, category, flavor).
    """
    mm.setCollection("candies")
    result = mm.get(
        query={"category": category},
        filter={"_id": 0, "name": 1, "price": 1, "category": 1},
    )
    return result

"4"
@app.get("/candies/desc/{keyword}")
def candies_by_description_keyword(keyword: str):
    """
    Get candies with a keyword in the description
    """
    return list(collection.find({"desc": {"$regex": keyword, "$options": "i"}},{"_id": 0, "name": 1, "price": 1, "category": 1, "desc": 1}))

"5"
@app.get("/candies/name/{keyword}")
def candies_by_name_keyword(keyword: str):
    """
    Get candies with a keyword in the name
    """
    return list(collection.find({"name": {"$regex": keyword, "$options": "i"}},{"_id": 0, "name": 1, "price": 1, "category": 1, "desc": 1}))

"6"
@app.get("/candies/price/{GTprice1}/{LTprice2}")
def candies_by_price_range(GTprice1: float, LTprice2: float):
    """
    Search for candies based on a price range
    """

    price_range_query = {"price": {"$gte": GTprice1, "$lte": LTprice2}}
    mm.setCollection("candies")
    rangeQuery = mm.get(
        query=price_range_query,
        filter={"_id": 0, "price": 1, "category_id": 1, "name": 1},
        sort_criteria={"price": -1},)
    return rangeQuery


"7"
@app.get("/candies/id/{id}")
def get_candy_by_id(id: str):
    """
    Get detailed information about a specific candy.
    """
    mm.setCollection("candies")
    result = mm.get(
        query={"id": id}, filter={"_id": 0, "name": 1, "price": 1, "category": 1}
    )
    return result

"9"
@app.put("/candies/price")
def update_candy_price(candy_id: str, updated_price: float):
    """
    Updates the price of an existing candy
    """
    mm.setCollection("candies")
    result = mm.put2("id", candy_id, "price", updated_price)  
    return result

"10"
@app.put("/candies/desc")
def update_candy_info(candy_id: str, updated_desc: str):
    """
    Update information about an existing candy.
    """
    mm.setCollection("candies")
    result = mm.put2("id", candy_id, "desc", updated_desc)  
    return result

"11"
@app.delete("/candies/{candy_id}")
def delete_candy(candy_id: str):
    """
    Remove a candy from the store's inventory.
    """
    return collection.delete_one({"id": candy_id})
    


@app.get("/promotions")
def promotions_and_deals():
    """
    Information about current promotions, deals, or discounts.
    """
    return "None ATM. Literally no way to pay for anything."


@app.get("/store-info")
def store_information():
    """
    Basic information about the candy store, including contact details.
    """
    return "This candy may or may not be laced. Contact @ no snitching."


"""
This main block gets run when you invoke this file. How do you invoke this file?

        python api.py 

On port 8084 because A04. 4!!!!!!!!!!!!!!!!!
After it is running, copy paste this into a browser: http://24.144.91.90:8084

You should see your api's base route!

Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    uvicorn.run(
        "api:app", host="24.144.91.90", port=8084, log_level="debug", reload=True
    )
"""                                   ^
                                      |
CHANGE DOMAIN NAME                    |              

"""
