```bash
docker-compose up --build -d
```
To navigate rest app please use:
https://www.usebruno.com

bruno collection in project file:
```bash
bruno/todo-bruno

```
ENDPOINTS:
```bash
auth:
# register panel
POST: http://localhost:5000/auth/register
# login panel
POST: http://localhost:5000/auth/login
# logout panel
POST http://localhost:5000/auth/logout

tasks:
# get all tasks for todo
GET: http://localhost:5000/todos/:todo_id/tasks
# get one task
GET: http://localhost:5000/tasks/:task_id
# create task
POST: http://localhost:5000/todos/:todo_id/tasks
# update task
PUT: http://localhost:5000/tasks/:task_id
# delete task
DELETE: http://localhost:5000/tasks/:task_id

todos:
# create todo
POST: http://localhost:5000/todos
# get one todo
GET: http://localhost:5000/todos/:id
# get all todos
GET: http://localhost:5000/todos
# update one todo
PUT: http://localhost:5000/todos/:id
# delete one todo
DELETE: http://localhost:5000/todos/:id
```

IMAGES:

![image](https://github.com/user-attachments/assets/e74782a3-90a2-4336-939e-27f3043d7328)
![image](https://github.com/user-attachments/assets/3a83ba0e-4638-4b5b-9a4a-15f59a3b155c)
![image](https://github.com/user-attachments/assets/9444022c-7b28-45f6-a652-34905033fd9a)
![image](https://github.com/user-attachments/assets/9fe83f57-d442-49d3-aaef-ef10bf35ebca)
![image](https://github.com/user-attachments/assets/21526fc2-37d7-427f-ac87-a95ee418c6bf)
![image](https://github.com/user-attachments/assets/486ad705-dcdf-4e54-bf68-fe4eb9b0fbbe)
![image](https://github.com/user-attachments/assets/cf075601-5c6d-429c-82f0-4b99696130f9)
![image](https://github.com/user-attachments/assets/ed1a5c2f-3bb3-4bcc-8026-d2988aeb9e0a)
