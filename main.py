import json
from ai import ai
from flask import Flask, render_template_string, render_template, request, redirect, make_response

with open("prompt.md", "r", encoding='utf-8') as file:
    prompt = file.read()

with open("credentials.json", "r") as file:
    credentials = json.load(file)

ai = ai(credentials["geminiKey"])
app = Flask(__name__)
model = "gemini-2.5-flash-lite"

@app.route('/prompt', methods = ['POST', 'GET']) 
def index():
    if request.method == 'POST': 
        user_prompt = request.form['prompt'] 
        resp = make_response(redirect("/")) 
        resp.set_cookie('prompt', user_prompt)
        return resp
    return render_template('index.html')

@app.errorhandler(404)
def test(error):
    user_prompt = request.cookies.get('prompt') 
    if not user_prompt:
        return redirect("/prompt")

    answer, error = ai.prompt(prompt=f"The user is at: {request.url} \n{user_prompt} \n{prompt}", model=model)
    if error:
        return render_template("error.html", code=error.code, message=error.message, status=error.status)

    code = ai.extract_code(answer)

    if code:
        return render_template_string(code)
    return "error"

if __name__=='__main__': 
   app.run(debug=True)