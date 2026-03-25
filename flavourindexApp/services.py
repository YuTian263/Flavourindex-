import os
import requests


def get_tasty_recipes(start=0, size=40):
    url = 'https://tasty.p.rapidapi.com/recipes/list' 

    headers = {
        "x-rapidapi-host":  'tasty.p.rapidapi.com', 
        "x-rapidapi-key": '803b2013c4mshd1f820d4b30b4f7p1eff1ajsn72c78c113cee'
    }

    params = {
        "from": start,
        "size": size,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        simplified_recipes = []

        for recipe in data.get("results", []):
            ingredients = []
            for section in recipe.get("sections", []):
                for component in section.get("components", []):
                    raw_text = component.get("raw_text")
                    if raw_text:
                        ingredients.append(raw_text)

            tags = []
            for tag in recipe.get("tags", []):
                display_name = tag.get("display_name")
                if display_name:
                    tags.append(display_name)

            simplified_recipes.append({
                'id' : None, 
                "source": "external",
                "title": recipe.get("name"),
                "description": recipe.get("description"),
                "cook_time_minutes": recipe.get("cook_time_minutes"),
                "ingredients": ingredients,
                "tags": tags,
                "picture": recipe.get("thumbnail_url"),
            })

        return simplified_recipes

    except requests.RequestException as e:
        print("Tasty API error:", e)
        return []