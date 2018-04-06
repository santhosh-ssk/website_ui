from flask import Flask,render_template,jsonify,request
from mongoengine import connect
import uuid
import base64,io
from data_model import User
connect(
    db='website_ui',
    username='admin',
    password='admin123',
    host='mongodb://admin:admin123@ds131384.mlab.com:31384/website_ui'
)

app=Flask(__name__)

Usernames=[user.username for user in User.objects().all()]
@app.route("/")
def home():
	return render_template('index.html',flash_message=None)
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
	#print(user.to_json())
	try:
		user.save()
		from data_model import User_token
		user_token=User_token(username=user_data['username'],token=str(uuid.uuid4())+str(uuid.uuid4()))
		user_token.save()
		Usernames.append(user_data['username'])
		return jsonify(response="success")
	except:
		return render_template('index.html',flash_message="User id exist")

@app.route("/login",methods=["POST"])
def login():
	login=request.form.to_dict()
	from data_model import User
	user=User.objects(username=login['username'],password=login['password']).first()
	if user:
		#print(base64.b64encode(user.profile_image.read()))
		return render_template('user.html',user={"name":user.name,"email":user.email,"phone":user.phone_no,"address":user.address,"dob":user.dob,"username":user.username},profile_image=(base64.b64encode(user.profile_image.read())).decode(),profile_image_type=user.profile_image_type)
		
	else:
		return render_template('index.html',flash_message="Invalid login id or password")

@app.route('/check_username_availability', methods=['POST'])
def check_username_availability():
	user_name=request.json['username']
	#print(Usernames,request.json)
	if user_name not in Usernames:
		return jsonify(response=1)
	else:
		return jsonify(response=0)
if __name__=="__main__":
	app.run(debug=True)