from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'a946c077239ccd9f76de70c4'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', codes = session.keys())

@app.route('/your-url', methods = ['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists("urls.json"):
            with open("urls.json") as url_file:
                urls = json.load(url_file)

        if request.form["code"] in urls.keys():
            flash("That short name has already been taken.")
            return redirect(url_for("home"))

        if "url" in request.form.keys():
              urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            relative_path = os.getcwd()
            f.save(relative_path + "\\static\\user_files\\" + full_name)
            urls[request.form['code']] = {'file': full_name}


        with open("urls.json", "w") as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code =  request.form["code"])
    else:
        return redirect(url_for("home"))


@app.route("/<string:code>")
def redirect_to_url(code):
    # check if the path exists
    if os.path.exists("urls.json"):
        # open the file as a variable
        with open("urls.json") as url_file:
            # create another variable and open it json up using the saved variable
            urls = json.load(url_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
                else:
                    return redirect(url_for("static", filename= "user_files/" + urls[code]["file"] ))


    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404