from orator import Model
from orator.orm import has_one
from orator.orm import has_many
from orator.orm import belongs_to
from orator.orm import has_many_through
from orator.orm import belongs_to_many
from orator.orm import scope
from orator.orm import accessor
from .connect import db


class Task(Model):
    __table__ = "tasks"
    __timestamps__ = "False"
    __fillable__ = ['channel', 'body']

    @has_many('task_id')
    def logics(self):
        return Logic

class Logic(Model):
    __table__ = "logics"
    __timestamps__ = "False"
    __fillable__ = ['task_id', 'percent', 'margin', 'val', 'title']


    @belongs_to('task_id')
    def task(self):
        return Task