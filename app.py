from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample food data (you can replace or expand this)
food_data = [
    {"name": "Doro Wot", "ingredients": ["chicken", "spices"], "calories": 450, "protein": 30, "fat": 20},
    {"name": "Lentil Salad", "ingredients": ["lentils", "tomato"], "calories": 350, "protein": 25, "fat": 10},
    {"name": "Avocado Toast", "ingredients": ["bread", "avocado"], "calories": 400, "protein": 10, "fat": 15}
]

# Route for the search page
@app.route("/search")
def search_page():
    return render_template("search.html")

# Handle search requests (from JavaScript)
@app.route("/search", methods=["POST"])
def search_food():
    data = request.json
    query = data.get("query", "").lower()
    search_type = data.get("type", "name")

    results = []

    if search_type == "name":
        results = [f for f in food_data if query in f["name"].lower()]
    elif search_type == "ingredient":
        results = [f for f in food_data if any(query in i for i in f["ingredients"])]
    elif search_type == "nutrition":
        if "high protein" in query:
            results = [f for f in food_data if f["protein"] >= 20]
        if "low fat" in query:
            results = [f for f in food_data if f["fat"] <= 10]
        if "under 400" in query:
            results = [f for f in food_data if f["calories"] < 400]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
