import os
import urllib.request
import json
from flask import Flask, request, redirect, jsonify, send_file ,send_from_directory
from werkzeug.utils import secure_filename
import pymysql

UPLOAD_FOLDER='C:\\Users\\karti\\Desktop\\Fourbrick\\images'


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'])

app = Flask(__name__)
def Connection():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1234',
                                db='fourbrick',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    #cursor = connection.cursor()
    return connection

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# if 'file' not in request.files:
		# 	resp = jsonify({'message' : 'No file part in the request'})
		# 	resp.status_code = 400
		# 	return resp
		
		files = request.files.getlist('files[]')
		resp=''
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)

				file.save(os.path.join(UPLOAD_FOLDER, filename))
				path=UPLOAD_FOLDER + "\\" +filename
				conn = Connection()
				cursor = conn.cursor()
				query = "INSERT INTO UploadFile (file,path) VALUES('" + filename + "','" + path + "')"
				cursor.execute(query)
				conn.commit()
				resp = jsonify({'message' : 'File successfully uploaded'})
				resp.status_code = 201
			else:
				resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
				resp.status_code = 400
		return resp		

@app.route('/download', methods=['POST'])
def downloadFile():
	if request.method == 'POST':
		data = request.get_data()
		data = json.loads(data.decode('utf-8'))

		query = 'select * from UploadFile where File="'+str(data['File'])+'"'
		conn = Connection()
		cursor = conn.cursor()
		cursor.execute(query)
		data1 = cursor.fetchone()
		os.open(data1['path'], os.O_RDWR | os.O_CREAT)
		return data1['path']

if __name__ == "__main__":
    app.run()