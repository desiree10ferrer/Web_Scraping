from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    marsnews = mongo.db.marsnews.find_one()
    return render_template("index.html", marsnews=marsnews)


@app.route("/scrape")
def scraper():
    marsnews = mongo.db.marsnews
    marsnews_data = scrape_mars.scrape1()
    marsnews_data = scrape_mars.scrape2()
    marsnews_data = scrape_mars.scrape3()
    marsnews_data = scrape_mars.scrape4()
    marsnews_data = scrape_mars.scrape5()
    marsnews.update({}, marsnews_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
