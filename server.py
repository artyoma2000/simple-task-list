from aiohttp import web
import json
import psycopg2

try:
    connection = psycopg2.connect(
        user='',
        password='',
        database='',
        host='',
        port=''
    )
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL database: {e}")

cursor = connection.cursor()


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_tasks(self):
        return self.tasks

    def duplicate_tasks(self):
        try:
            cursor.execute("TRUNCATE tasks")
            for task in self.tasks:
                cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
            connection.commit()
        except psycopg2.Error as e:
            print(f"Error duplicating tasks: {e}")

    def read_tasks(self):
        try:
            cursor.execute("SELECT task FROM tasks")
            self.tasks = [row[0] for row in cursor.fetchall()]
        except psycopg2.Error as e:
            print(f"Error reading tasks: {e}")


async def get_tasks(request):
    try:
        todo_list.read_tasks()
        tasks = todo_list.get_tasks()
        return web.Response(text=json.dumps(tasks))
    except Exception as e:
        return web.Response(status=500, text=f"Error retrieving tasks: {e}")


async def add_task(request):
    try:
        todo_list.read_tasks()
        data = await request.json()
        task = data.get('tasks')
        todo_list.add_task(task)
        todo_list.duplicate_tasks()
        return web.Response(text='Task added')
    except Exception as e:
        return web.Response(status=500, text=f"Error adding task: {e}")


async def remove_task(request):
    try:
        data = await request.json()
        task = data.get('tasks')
        todo_list.remove_task(task)
        todo_list.duplicate_tasks()
        return web.Response(text='Task removed')
    except Exception as e:
        return web.Response(status=500, text=f"Error removing task: {e}")


async def update_tasks(request):
    try:
        data = await request.json()
        tasks = data.get('tasks')
        todo_list.tasks = tasks
        todo_list.duplicate_tasks()
        return web.Response(text='Tasks updated')
    except Exception as e:
        return web.Response(status=500, text=f"Error updating tasks: {e}")


todo_list = TodoList()

app = web.Application()
app.router.add_get('/tasks', get_tasks)
app.router.add_post('/tasks', add_task)
app.router.add_delete('/tasks', remove_task)
app.router.add_put('/tasks', update_tasks)

web.run_app(app, port=8080)
