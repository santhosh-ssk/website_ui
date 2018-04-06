from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/first_map")
def map():
	return render_template('first_map.html')

if __name__=="__main__":
	app.run(debug=True)