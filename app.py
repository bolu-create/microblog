from flask import Flask, render_template, request
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime


load_dotenv()

def create_app():
    app = Flask(__name__)
    client= MongoClient(os.getenv("MONGODB_URI"))#put in your mongodb connection url
    app.db = client.Microblog #connect to the database using app.db to save microblog connection inside "app"

    #entries = []

    @app.route("/", methods=["GET","POST"])
    def home():
        
        #entries=[] # part of my own solution. Resets the list everytime the route is called. entries was outside cause we were saving
        #more than one entry with hardcoding at the time.
        #app.db.entries_db.find({}) #access the collection you created in the db. finds all in your collection and gives is back to you
        #print([e for e in app.db.entries_db.find({})]) # printing or retrive from the db a list of things in my collection in the db. to check if db is connected
        
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date= datetime.datetime.today().strftime("%Y-%m-%d")
            #entries.append((entry_content, formatted_date,datetime.datetime.today()))
            app.db.entries_db.insert_one({"content":entry_content, "date":formatted_date})
            
        # instructors solution
        entries_with_date= [
            (
            entry['content'],
            entry['date'],
            datetime.datetime.strptime(entry['date'], "%Y-%m-%d").strftime("%b %d") 
            ) for entry in app.db.entries_db.find({})   
        ]
        
        """
        #retriving the data from mongodb and running it in my app. [MY ATTEMPT]  
        for item in app.db.entries_db.find({}):
            
            content= item['content']
            date= item['date']
            
            entries.append((content, date, datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%b %d")))
        """
    
        """
        # I need to check this again    
        entries_with_date= [
            (
            entry[0],
            entry[1],
            datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d") 
            ) for entry in entries   
        ]
        """
        
        return render_template("home.html", entries= entries_with_date)
        #return render_template("home.html", entries= entries)
    
    return app

