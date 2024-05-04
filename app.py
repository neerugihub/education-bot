from flask import Flask, render_template, request
import requests
from pydantic import BaseModel, Field
from typing import List, Optional

# Define models for book details
class Book(BaseModel):
    ISBN: str
    author: str
    description: str
    img_link: str
    pdf_link: str
    publisher: str
    title: str
    year: str

class BookSearchResponse(BaseModel):
    results: List[Book]

# Now you can use these models to parse the API response
def parse_book_search_response(response):
    return BookSearchResponse.parse_obj(response)

# Use the models to fetch and parse the API response
def fetch_books_info(query):
    url = "https://getbooksinfo.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "e3a26d3d91msh1df956f0cff2a43p1c4efbjsn35d8a93e0c81",
        "X-RapidAPI-Host": "getbooksinfo.p.rapidapi.com"
    }
    querystring = {"s": query}

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return parse_book_search_response(response.json())
    else:
        return None

# Initialize Flask app
app = Flask(__name__)

# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        book_query = request.form['book_query']
        book_search_response = fetch_books_info(book_query)
        if book_search_response and book_search_response.results:
            return render_template('results.html', results=book_search_response.results)
        else:
            return render_template('error.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
