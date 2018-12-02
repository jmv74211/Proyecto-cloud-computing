# -*- coding: utf-8 -*-

# Clase gestionar un conjunto de tareas
class Task:

    task_num = 1

    def __init__(self,_user, _task_name, _task_estimation, _task_difficulty, _task_max_date):
        self.task_id = Task.task_id
        Task.task_id += 1
        self.user = _user
        self.task_name = _task_name
        self.task_estimation = _task_estimation
        self.task_difficulty = _task_difficulty
        self.task_max_date = _task_max_date
