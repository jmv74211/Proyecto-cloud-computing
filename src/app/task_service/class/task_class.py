# -*- coding: utf-8 -*-

# Clase gestionar un conjunto de tareas
class Task:

    task_num = 1

    def __init__(self,_user, _task_name, _task_description, _task_estimation, _task_difficulty, _task_max_date):
        self.task_id = Task.task_num
        Task.task_num += 1
        self.user = _user
        self.task_name = _task_name
        self.task_description = _task_description
        self.task_estimation = _task_estimation
        self.task_difficulty = _task_difficulty
        self.task_max_date = _task_max_date

    def to_dict(self):
        return self.__dict__
