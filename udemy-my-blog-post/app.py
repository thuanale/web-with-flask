#!/usr/bin/env python3

from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING

def create_app():
    app=Flask(__name__)
    client = MongoClient("mongodb://mongo:mongo@db:27017")
    app.db = client["microblog"]
    collection = app.db["posts"]

    @app.route("/", methods=["GET","POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            collection.insert_one({
                "content": entry_content,
                "date": formatted_date,
            })

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d")
            )
            for entry in collection.find({}).sort([("date", DESCENDING)])
        ]
        return render_template("home.html", entries=entries_with_date)
    
    return app