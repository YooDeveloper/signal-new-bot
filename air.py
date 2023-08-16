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
    logics = F.LinkField("logics", ".Logic")  # option 1

    class Meta:
        base_id = "appkufJyNyxL0SMxm"
        table_name = "tasks"
        api_key = API_KEY

class Logic(Model):
    title = F.TextField("Title")
    percent = F.IntegerField("percent")
    margin = F.IntegerField("margin")
    val = F.IntegerField("val")
    task = F.LinkField("tasks", Task)

    class Meta:
        base_id = "appkufJyNyxL0SMxm"
        table_name = "logics"
        api_key = API_KEY

# for task in Task.all():
#     for logic in task.logics:
#         print(logic.percent)
