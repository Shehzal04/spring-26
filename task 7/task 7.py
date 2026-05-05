import requests
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

BASE_URL            = "https://www.themealdb.com/api/json/v1/1"
TIMEOUT             = 8    # seconds for every outbound request
MAX_SEARCH          = 5    # max recipes returned on ingredient search
MAX_ING_SEARCH      = 10   # max ingredients shown in search results
MAX_ING_RANDOM      = 15   # max ingredients shown for random recipe
PREVIEW_LEN_SEARCH  = 300  # instruction preview length for search
PREVIEW_LEN_RANDOM  = 500  # instruction preview length for random

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe Finder</title>
    <style>
        :root {
            --accent:  #ff6b35;
            --bg:      #fff5e6;
            --card-bg: #ffffff;
            --ing-bg:  #f9f9f9;
            --radius:  8px;
            --shadow:  0 2px 5px rgba(0,0,0,.1);
        }

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: Arial, sans-serif;
            background: var(--bg);
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        h1 { margin-bottom: 20px; }

        .search-box {
            text-align: center;
            margin: 20px 0;
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        input, button {
            padding: 10px 14px;
            border-radius: var(--radius);
            border: 1px solid #ccc;
            font-size: 1em;
        }

        button {
            background: var(--accent);
            color: #fff;
            border: none;
            cursor: pointer;
            transition: opacity .2s;
        }
        button:hover { opacity: .85; }

        .recipe-card {
            background: var(--card-bg);
            padding: 20px;
            margin: 15px 0;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
        }

        .recipe-title { font-size: 1.5em; color: var(--accent); margin-bottom: 10px; }
        .recipe-image { max-width: 200px; border-radius: 5px; margin: 10px 0; display: block; }

        .ingredients {
            background: var(--ing-bg);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }

        .ingredients h3, .recipe-card h3 { margin-bottom: 6px; }
        .ingredients ul { padding-left: 20px; }
        .ingredients li { margin: 3px 0; }

        .recipe-card p { margin: 6px 0; line-height: 1.5; }
        .recipe-card a { color: var(--accent); }

        #status { text-align: center; color: #888; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1> Recipe Finder</h1>

        <div class="search-box">
            <input type="text" id="ingredient" placeholder="Enter ingredient (e.g., chicken)">
            <button onclick="searchRecipes()">Search Recipes</button>
            <button onclick="getRandomRecipe()">Random Recipe</button>
        </div>

        <p id="status"></p>
        <div id="results"></div>
    </div>

    <script>
        const status  = document.getElementById('status');
        const results = document.getElementById('results');

        function setStatus(msg) { status.textContent = msg; }

        function buildRecipeHTML(recipe) {
            const ings = recipe.ingredients.map(ing => `<li>${ing}</li>`).join('');
            return `
                <div class="recipe-card">
                    <h2 class="recipe-title">${recipe.name}</h2>
                    <img src="${recipe.image}" class="recipe-image" alt="${recipe.name}">
                    <p><strong>Category:</strong> ${recipe.category}</p>
                    <p><strong>Area:</strong> ${recipe.area}</p>
                    <div class="ingredients">
                        <h3>Ingredients:</h3>
                        <ul>${ings}</ul>
                    </div>
                    <h3>Instructions:</h3>
                    <p>${recipe.instructions}</p>
                    <a href="${recipe.source}" target="_blank" rel="noopener">View Full Recipe</a>
                </div>`;
        }

        function displayRecipes(data) {
            if (data.error) {
                results.innerHTML = `<p>Error: ${data.error}</p>`;
            } else if (data.meals && data.meals.length) {
                results.innerHTML = data.meals.map(buildRecipeHTML).join('');
            } else {
                results.innerHTML = '<p>No recipes found.</p>';
            }
            setStatus('');
        }

        async function fetchAndDisplay(url) {
            setStatus('Loading…');
            results.innerHTML = '';
            try {
                const res  = await fetch(url);
                const data = await res.json();
                displayRecipes(data);
            } catch (err) {
                results.innerHTML = `<p>Network error: ${err.message}</p>`;
                setStatus('');
            }
        }

        function searchRecipes() {
            const ingredient = document.getElementById('ingredient').value.trim();
            if (!ingredient) { alert('Please enter an ingredient.'); return; }
            fetchAndDisplay(`/recipes?ingredient=${encodeURIComponent(ingredient)}`);
        }

        function getRandomRecipe() {
            fetchAndDisplay('/random-recipe');
        }
    </script>
</body>
</html>
"""

def _get(url: str) -> dict:
    """GET *url* with a fixed timeout; raises on HTTP errors."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def _extract_ingredients(meal: dict, limit: int) -> list:
    """Return up to *limit* non-empty 'measure + ingredient' strings from a meal dict."""
    ingredients = []
    for i in range(1, 21):
        ing     = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}")    or "").strip()
        if ing:
            ingredients.append(f"{measure} {ing}".strip())
        if len(ingredients) == limit:
            break
    return ingredients


def _format_meal(meal: dict, preview_len: int, ing_limit: int) -> dict:
    """Serialize a raw MealDB meal dict into our API response shape."""
    return {
        "name":         meal["strMeal"],
        "category":     meal["strCategory"],
        "area":         meal["strArea"],
        "instructions": meal["strInstructions"][:preview_len] + "…",
        "image":        meal["strMealThumb"],
        "source":       meal.get("strSource") or "#",
        "ingredients":  _extract_ingredients(meal, ing_limit),
    }

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/recipes")
def search_recipes():
    ingredient = request.args.get("ingredient", "").strip()
    if not ingredient:
        return jsonify({"error": "Please provide an ingredient."})

    try:
        data  = _get(f"{BASE_URL}/filter.php?i={ingredient}")
        meals = data.get("meals")
        if not meals:
            return jsonify({"error": "No recipes found."})

        recipes = []
        for meal in meals[:MAX_SEARCH]:
            detail = _get(f"{BASE_URL}/lookup.php?i={meal['idMeal']}")
            if detail.get("meals"):
                recipes.append(
                    _format_meal(detail["meals"][0], PREVIEW_LEN_SEARCH, MAX_ING_SEARCH)
                )

        return jsonify({"meals": recipes})

    except requests.RequestException as e:
        return jsonify({"error": f"Request failed: {e}"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/random-recipe")
def random_recipe():
    try:
        data  = _get(f"{BASE_URL}/random.php")
        meals = data.get("meals")
        if not meals:
            return jsonify({"error": "Failed to get a random recipe."})

        return jsonify({"meals": [_format_meal(meals[0], PREVIEW_LEN_RANDOM, MAX_ING_RANDOM)]})

    except requests.RequestException as e:
        return jsonify({"error": f"Request failed: {e}"})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
