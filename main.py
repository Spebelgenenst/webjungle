import json
from ai import ai
from flask import Flask, render_template_string, render_template, request, redirect, make_response
from flask_session import flask_session

with open("prompt.md", "r", encoding="utf-8") as file:
    prompt = file.read()

with open("credentials.json", "r") as file:
    credentials = json.load(file)

with open("config.json", "r") as file:
    config = file.read()

ai = ai(credentials["geminiKey"])
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
model = "gemini-2.5-flash-lite"

@app.route(config["goal"])
def goal():
    referer = request.headers.get('Referer')
    if referer and referer.startswith(request.host_url):
        return "you made it!"
    return " you are disqualified for cheating! >:c"

@app.route("/prompt", methods = ["POST", "GET"]) 
def index():
    if request.method == "POST": 
        user_prompt = request.form["prompt"] 
        resp = make_response(redirect("/")) 
        resp.set_cookie("prompt", user_prompt)
        return resp
    return render_template("index.html")

@app.errorhandler(404)
def test(error):
    user_prompt = request.cookies.get("prompt") 
    if not user_prompt:
        return redirect("/prompt")

    answer, error = ai.prompt(prompt=f"The user is at: {request.url} \n{user_prompt} \n{prompt}", model=model)
    if error:
        return render_template("error.html", code=error.code, message=error.message, status=error.status)

    code = ai.extract_code(answer)

    if not code:
        return render_template("error.html", code="UWU", message="There was no code in the ai's response.", status="NO_CODE")
    return render_template_string(code)

if __name__=="__main__": 
   app.run(debug=True)