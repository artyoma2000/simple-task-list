from aiohttp import web
import json


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_tasks(self):
        return self.tasks


# Получить список задач
async def get_tasks(request):
    tasks = todo_list.get_tasks()
    return web.Response(text=json.dumps(tasks))


# Добавить задачу
async def add_task(request):
    data = await request.json()
    task = data.get('task')
    todo_list.add_task(task)
    return web.Response(text='Task added')


# Удалить задачу
async def remove_task(request):
    data = await request.json()
    task = data.get('task')
    todo_list.remove_task(task)
    return web.Response(text='Task removed')


# Обновить список задач
async def update_tasks(request):
    data = await request.json()
    tasks = data.get('tasks')
    todo_list.tasks = tasks
    return web.Response(text='Tasks updated')


todo_list = TodoList()

app = web.Application()
app.router.add_get('/tasks', get_tasks)
app.router.add_post('/tasks', add_task)
app.router.add_delete('/tasks', remove_task)
app.router.add_put('/tasks', update_tasks)


web.run_app(app, port=8080)