#!flask/bin/python
#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

from flask import Flask, jsonify

from flask import abort
from flask import make_response
from flask import request
from flask import render_template,send_from_directory



import sys
if sys.version_info[0] >= 3:
    unicode = str

app = Flask(__name__,static_url_path='')


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/assets/<path:path>')
def send_imagetest(path):
    response = make_response(send_from_directory('templates', path))
    response.headers['Cache-Control'] = 'public,max-age=0s,must-revalidate'
    del response.headers['Expires']
    return response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/create/task', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    newtask = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    found = False
    for task in tasks:
        if task['title'] == newtask['title']:
            found = True
            abort(400,{'message': 'Already the Task Exists in the Database'})
    
    if found == False:
        tasks.append(newtask)
        return jsonify({'task': newtask}), 201


@app.route('/todo/api/update/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        print("check here 1")
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        print("Failing1")
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        print("Failing2")
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        print("Failing3")
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/delete/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.route('/todo/api/list/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/todo/api/list/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/list/methods', methods=['OPTIONS'])
def get_methods():
    resp = make_response("",204)
    resp.headers['Allow'] = 'OPTIONS,GET,PUT,POST,HEAD,DELETE'
    return resp  

@app.route('/testredirect301', methods=['GET'])
def issueredirect301():
    resp = make_response("",301)
    resp.headers['location'] = 'http://www.google.com'
    return resp  


@app.route('/testredirect302', methods=['GET'])
def issueredirect302():
    resp = make_response("",302)
    resp.headers['location'] = 'https://www.ndtv.com'
    return resp  


@app.route('/testcustommethod', methods=['BULLI'])
def customMethodforBulli():
    resp = make_response("This is an output of Custom Method",200)
    return resp  


@app.route('/testcustomStatusCode', methods=['BULLI'])
def customStatusCodeforBulli():
    resp = make_response("This is an output of Custom Status Code",777)
    return resp  

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True,host='0.0.0.0', port=80)


'''
echo '{"title":"Read a book","description":"Read a Story Book","done":"False"}' | http POST http://localhost:5000/todo/api/create/task

http GET http://localhost:5000/todo/api/list/tasks -v
http HEAD  http://www.geethapriya.xyz:5000/todo/api/list/tasks -v

http POST http://localhost:5000/todo/api/create/task -v <<< '{"title":"Reading","description":"Read a Story Book","done":false}'
http POST http://localhost:5000/todo/api/create/task -v <<< '{"title":"Playing","description":"Play Football","done":false}'

http PUT http://localhost:5000/todo/api/update/task/3 -v <<< '{"title":"Reading","description":"Read a Story Book","done":true}'

http OPTIONS http://localhost:5000/todo/api/list/methods -v

http DELETE http://localhost:5000/todo/api/delete/tasks/3 -v


Response Codes:
http POST http://localhost:5000/todo/api/create/task -v <<< '{"title":"Reading,"description":"Read a Story Book","done":"False"}'


http POST http://localhost:5000/todo/api/create/task -v <<< '{"title":"Reading","description":"Read a Story Book","done":"False"}'
'''