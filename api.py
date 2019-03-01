from flask import Flask, url_for, send_from_directory, request, jsonify
import logging, os
from werkzeug import secure_filename
import json
from pathlib import Path

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/upload', methods = ['POST'])
def upload_api():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        
        return json.dumps({'filename':img_name,'carbs':'10','salt':'10','liquid':'2'})
    else:
        return "Incorrect upload request.... :("

@app.route('/status', methods = ['GET'])
def status_api():
    app.logger.info(PROJECT_HOME)
    
    id=request.args.get('id')
    resp_file=Path("downloads/"+ id +".json")
    app.logger.info("Processing request for id" + id )

    if resp_file.exists():
        app.logger.info("Found results for id:" + id )
        return send_from_directory("downloads", id+".json")
    else:   
        app.logger.info("Results not found  for id:" + id )
        return jsonify(status="In-progress" )

@app.route('/download', methods = ['GET'])
def download_api():
    app.logger.info(PROJECT_HOME)
    
    id=request.args.get('id')
    resp_file=Path("downloads/"+ id +".png")
    app.logger.info("Processing request for id" + id )

    if resp_file.exists():
        app.logger.info("Found results for id:" + id )
        return send_from_directory("downloads", id + ".png")
    else:   
        app.logger.info("Not found results for id:" + id )
        return jsonify(status="In-progress" )


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=False)