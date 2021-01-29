from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_so_jobs
from exporter import *

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        fromdb = db.get(word)
        if fromdb:
            jobs = fromdb
        else:
            jobs = get_so_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")

    return render_template(
        "report.html", resultsNumber=len(jobs), SearchingBy=word,jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word=word.lower()
    jobs=db.get(word)

    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")  
  except:
    return redirect("/")


app.run(host="0.0.0.0")
