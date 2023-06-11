from flask import Flask, render_template, request, url_for, jsonify
import bookSearch
import recommender

app = Flask(__name__)

@app.route("/")
def home():
    # Render index.html template
    return render_template("index.html")

@app.route("/perform-search", methods=['POST'])
def perform_search():
    # Handle search request, return search results as JSON
    data = request.get_json()
    searchTerm = data['searchTerm']
    result = (bookSearch.search(searchTerm)).tolist()
    return jsonify(result)

@app.route("/perform-recs", methods=['POST'])
def perform_recs():
    # Handle recommendations request, return combined book IDs and titles as JSON
    data = request.get_json()
    selectedBooks = data['selectedBooks']
    result = recommender.get_recs(selectedBooks)
    titleList = result["title"].tolist()
    idList = result["book_id"].tolist()
    res = []
    for item1, item2 in zip(titleList, idList):
        combined_item = f"{item2} {item1}"
        res.append(combined_item)
    return jsonify(res)

@app.route('/mylist')
def new_page():
    # Render list.html template
    return render_template('list.html')

if __name__ == '__main__':
    # Start Flask development server with debug mode enabled
    app.run(debug=True)
