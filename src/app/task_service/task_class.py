# -*- coding: utf-8 -*-

import task_model as model


# Clase gestionar un conjunto de tareas
class Task:

    def __init__(self,_user, _task_name, _task_description, _task_estimation, _task_difficulty, _task_max_date):
        self.task_id = model.get_next_task_id()
        self.user = _user
        self.name = _task_name
        self.description = _task_description
        self.estimation = _task_estimation
        self.difficulty = _task_difficulty
        self.max_date = _task_max_date

    def to_dict(self):
        return self.__dict__
