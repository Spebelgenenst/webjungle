from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/feuer')
def feuer():
    referer = request.headers.get('Referer')
    if not referer:
        return 
    if referer.startswith(request.host_url):
        return ":mogg:"
    if referer:
        return f"Du bist von {referer} hierher gekommen (Linkklick)." + request.url
    else:
        return "Du hast die URL wahrscheinlich manuell eingegeben."

@app.route("/mogg")
def index():
    return render_template_string("""
    <a href="/feuer">test</a>
    """)

if __name__=='__main__': 
   app.run(debug=True)