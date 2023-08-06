#!/usr/bin/python3

import requests,feedparser
from bs4 import BeautifulSoup
import json
class _SaveRecipe(object):
    def __init__(self):
        pass
class chefkoch:
    def __init__(self):
        pass

    def daily_recipe(self):
        feed = feedparser.parse("https://www.chefkoch.de/rss/rezept-des-tages.php")
        url = feed['entries'][0]['link']
        recipe = self._get(url.split("/")[4])
        return(recipe)

    def _get(self,recipe_id):
        url = "https://www.chefkoch.de/rezepte/"+ str(recipe_id)
        recipe = _SaveRecipe()
        content = BeautifulSoup(requests.get(url).text, 'html.parser')
        recipe_json = json.loads(content.findAll("script",type="application/ld+json")[1].string)
        for item in ["name", "recipeInstructions", "image", "recipeIngredient", "recipeCategory", "datePublished", "prepTime", "recipeYield", ["aggregateRating", "ratingValue"], ["aggregateRating", "reviewCount"]]:
            if type(item) == str:
              recipe_json.setdefault(item, None)
            else:
              recipe_json.setdefault(item[0], dict())
              recipe_json[item[0]].setdefault(item[1], None)

        recipe.name = recipe_json["name"]
        recipe.description = recipe_json["recipeInstructions"]
        recipe.image = recipe_json["image"]
        recipe.ingredients = recipe_json["recipeIngredient"]
        try:
          recipe.rating = float(recipe_json["aggregateRating"]["ratingValue"])
        except:
          recipe.rating = recipe_json["aggregateRating"]["ratingValue"]
        recipe.category = recipe_json["recipeCategory"]
        recipe.published = recipe_json["datePublished"]
        recipe.cooktime = recipe_json["prepTime"]
        recipe.autor = recipe_json["author"]["name"]
        recipe.reviews = recipe_json["aggregateRating"]["reviewCount"]
        recipe._yield = recipe_json["recipeYield"]
        recipe.id = recipe_id
        recipe.url = url
        #recipe.calories = recipe_json["nutrition"]["calories"]
        return recipe

    def search(self, search, limit=10, offset=0):
        result = list()
        url = "https://www.chefkoch.de/rs/s0/"+search+"/Rezept.html"
        content = BeautifulSoup(requests.get(url).text, 'html.parser')
        objects = json.loads(content.findAll('script', type='application/ld+json')[1].string)["itemListElement"]
        for recipe in objects[offset:limit]:
            result += [self._get(recipe["url"].split("/")[4])]
        return(result)
