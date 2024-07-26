from flask import Flask, request, render_template, redirect, url_for, make_response
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("test_render")) # this works

@app.route("/test_render/")
def test_render():
    name = request.args.get("name")
    if not name: name = "No Name"

    # return render_template("index_simple.html", person=name)

    # returning the line above did nothing, so I tried this instead in case it was a caching problem, but it still doesn't work
    # originally from a stack overflow post I couldn't find, but found this which explains it: https://stackoverflow.com/questions/49547/how-do-we-control-web-page-caching-across-all-browsers
    response = make_response(render_template("index_simple.html", person=name))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/test_redirect/")
def test_redirect():
    r = int(request.args.get("r")) if request.args.get("r") else 0
    name = request.args.get("name")
    if not name: name = "No Name"
    
    if r == 1:
        url = url_for(".test_redirect", name="Bob")
        print(f"redirecting to '{url}'...", file=sys.stderr)
        return redirect(url, code=302)
    else:
        print("rendering...", file=sys.stderr)

        return render_template("index_simple.html", person=name)
        # i also tried the caching solution shown above here but it didn't change anything