from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import datetime

app = Flask(__name__)

with open("./json/books.json", encoding='utf8') as jsonFile:
    books = json.load(jsonFile)
    jsonFile.close()

current_user = ["", ""]


@app.route('/')
def hello_world():
    return render_template('index.html', title='Авторизация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        current_user[0] = request.form['nick']
        current_user[1] = request.form['password']
    return render_template('list.html', books=books, user=current_user[0], password=current_user[1])


@app.route('/book/<string:name>', methods=['GET', 'POST'])
def book(name):
    book = None
    for item in books:
        if item["title"] == name:
            book = item
    return render_template("book.html", book=book, user=current_user[0], password=current_user[1])


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    books.append({
        "id": len(books) + 1,
        "title": request.form["title"],
        "author": request.form["author"],
        "year": request.form["year"],
        "date_of_taking": "",
        "date_of_return": "",
        "user": "",
        "description": request.form["description"]
    })
    return redirect('/login')


@app.route('/filter/<string:id>')
def filter(id):
    titles = []
    if id == '01':
        for item in books:
            titles.append({"id": item["id"], "status": True})
    elif id == '02':
        for item in books:
            status = True
            if item["date_of_taking"] != "":
                status = False
            titles.append({"id": item["id"], "status": status})
    elif id == "03":
        for item in books:
            status = True
            if item["date_of_taking"] == "":
                status = False
            titles.append({"id": item["id"], "status": status})
    return jsonify(titles)


@app.route('/remove/<string:id>')
def remove(id):
    for item in books:
        if item['id'] == int(id):
            books.remove(item)
            return redirect('/login')
    return redirect('/login')


@app.route("/edit/<string:id>", methods=['GET','POST'])
def edit(id):
    index = int(id)
    for item in books:
        if item['id'] == index:
            item['title'] = request.form['title']
            item['year'] = request.form['year']
            item['author'] = request.form['author']
            item['description'] = request.form['description']
    return redirect('/login')


@app.route("/take/<string:id>", methods=['GET','POST'])
def take(id):
    for item in books:
        if item['id'] == int(id):
            if request.form['user']:
                item["user"] = request.form['user']
                item['date_of_taking'] = str(datetime.datetime.now()).split()[0]
                item['date_of_return'] = request.form['date_of_return']
                return redirect('/login')
    return redirect('/login')


@app.route("/return/<string:id>", methods=['GET','POST'])
def return_book(id):
    for item in books:
        if item['id'] == int(id):
            item["user"] = ""
            item['date_of_taking'] = ""
            item['date_of_return'] = ""
            return redirect('/login')
    return redirect('/login')


if __name__ == '__main__':
    app.run()