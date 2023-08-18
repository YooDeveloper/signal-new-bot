from pyairtable import Api, Table
from pyairtable.orm import Model, fields as F

api = Api('patkRETuzVwQakwqC.f8da454447f31686a97c131ce484d804246cf797f9173464fa2315764f5c9a40')
API_KEY = 'patkRETuzVwQakwqC.f8da454447f31686a97c131ce484d804246cf797f9173464fa2315764f5c9a40'
# table = api.table('appkufJyNyxL0SMxm', 'tbl1wPzfC6DaS3ZcV')
# print(table.all())

# table.create({"Name": "Bob"})


class Task(Model):
    name = F.TextField("Name")
    channel = F.TextField("channel")
    body = F.TextField("body")
    packages = F.LinkField("packages", ".Package")  

    class Meta:
        base_id = "appkufJyNyxL0SMxm"
        table_name = "tasks"
        api_key = API_KEY

class Package(Model):
    name = F.TextField("Name")
    var_count = F.IntegerField("Количество переменных")
    template = F.AttachmentsField("Шаблон")

    tasks = F.LinkField("tasks", Task)
    logics = F.LinkField("logics", ".Logic")  

    class Meta:
        base_id = "appkufJyNyxL0SMxm"
        table_name = "packages"
        api_key = API_KEY

class Logic(Model):
    title = F.TextField("Title")
    percent = F.FloatField("Процент")
    margin = F.IntegerField("Накрутка руб")
    val = F.IntegerField("Делитель")
    last_val = F.FloatField("last_val")
    packages = F.LinkField("packages", Package)

    class Meta:
        base_id = "appkufJyNyxL0SMxm"
        table_name = "logics"
        api_key = API_KEY


def calculate_from_logic(task_id: str, input_from_api: float):
    task = Task.from_id(task_id)
    for package in task.packages:
        var_count = package.var_count
        if var_count == 1:
            pass
        elif var_count == 2:
            pass
        else:
            pass
        for logic in package.logics:
            print(logic)
    return task

# for task in Task.all():
#     for package in task.packages:
#         print(package)

print(calculate_from_logic('recnIckOiLGzm8r3P', 96.2))