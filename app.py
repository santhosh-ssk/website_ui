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
	file=request.files.to_dict()['file']
	from data_model import User
	user=User(**user_data)
	user.profile_image.put(file.read())
	user.profile_image_name=file.filename
	user.profile_image_type=file.filename.split('.')[1]
	print(user.to_json())
	user.save()

	return jsonify(response="success")
if __name__=="__main__":
	app.run(debug=True)