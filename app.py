from flask import Flask,render_template,jsonify,request
from mongoengine import connect
connect(
    db='website_ui',
    username='admin',
    password='admin123',
    host='mongodb://admin:admin123@ds131384.mlab.com:31384/website_ui'
)

app=Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')
@app.route("/signup",methods=["POST"])
def signup():
	user_data=request.form.to_dict()
	user_data.pop('confirm_password')
	print(user_data,request.files.to_dict())

	return jsonify(response="success")
if __name__=="__main__":
	app.run(debug=True)