# get_chefkoch
<a href="http://pepy.tech/count/get-chefkoch"><img src="http://pepy.tech/badge/get-chefkoch"></a> <a href="https://badge.fury.io/py/get-chefkoch"><img src="https://badge.fury.io/py/get-chefkoch.svg" alt="PyPI version" height="18"></a> <a href="https://github.com/olzeug/get_chefkoch/blob/master/LICENSE"><img src="https://img.shields.io/github/license/olzeug/get_chefkoch.svg"></a><br>
A Python Library with which you can get data from Chefkoch.

Example:
--------

```python
from get_chefkoch import chefkoch

c = chefkoch()
recipe = c.daily_recipe()
print(recipe.name)
```

```python
from get_chefkoch import chefkoch

c = chefkoch()
print(c.search("Hot Dog").id)
```
Features:
--------

- Query the recipe of the day
- Search for specific recipe
- Querying information about a recipe(cooking time, description, ingredients, ...)

Get it now:
----------

```
pip install get-chefkoch
```
