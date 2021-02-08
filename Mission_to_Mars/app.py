from flask import Flask, render_template, redirect
import pymongo 
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars

col = db.data

@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape()
    col.insert_one(mars_data)
    print("start")
    print (list(col.find()))
    print("finish")
    return redirect("/")


@app.route("/")
def home():
    
    data = col.find_one()
    return render_template("index.html", mars=data)


if __name__ == "__main__":
    app.run(debug=True)


