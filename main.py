import json
import PySimpleGUI as sg
from PySimpleGUI import Window, Button, Text, InputText
from PySimpleGUI.PySimpleGUI import Cancel, Listbox, Input, TabGroup, Tab
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Johnisa1997:Kladdkaka97@trainingdata.6ltsv.mongodb.net/test")
db = client["Personal_Bests"]
db["John"]
db["Elin"]

sg.theme('topanga')
scoreboard = sg.Listbox(values=[" "," "," "], key='Scoreboard', enable_events=True, size=(30,10), no_scrollbar=True)
date = Text(size=(10,1))

new_user = sg.Combo(db.list_collection_names(), size=(10,1), readonly=True, key="user_list")
scoreboard_user = sg.Combo(db.list_collection_names(), size=(10,1), readonly=True, key="user_choice", enable_events=True)
user_delete_instance = sg.Combo(db.list_collection_names(), size=(10,1), readonly=True, key="user_deletor", enable_events=True)
delete_instances_list = sg.Combo(["","",""], size=(10,1), readonly=True, key="delete_instance_list")

calendar = sg.In(key='calendar', enable_events=True, visible=False)
new_date = sg.CalendarButton('Calendar', target='calendar', pad=None, font=('MS Sans Serif', 10, 'bold'),
                 key='_CALENDAR_', format=('%Y-%m-%d'))
show_new_date = Text(size=(10,1))
new_exercise = Input(size=(10,1))
new_score = Input(size=(10,1))
new_set = Input(size=(10,1))
new_rep = Input(size=(10,1))
new_unit = Input(size=(10,1))

new_workout_picture = sg.FileBrowse('Browse', file_types=(("Images", "*.jpg"),), initial_folder=r"C:\Users\John\Desktop", target="workout_picture")
#main window
Insert_layout = [[Text("Enter new record")], 
                [Text("User:", size=(12,1)), new_user],
                [Text("Excersise name:", size=(12,1)), new_exercise],
                [Text("Personal best:", size=(12,1)), new_score],
                [Text("Sets:", size=(12,1)), new_set],
                [Text("Reps:", size=(12,1)), new_rep],
                [Text("Unit:", size=(12,1)), new_unit],
                [Text("Date:"), calendar, new_date, show_new_date],
                [Button("Submit")]]

Search_layout = [[Text("Search old record")],
                [scoreboard_user],
                [scoreboard],
                [Button('Update')], 
                [Text("Date:", size=(12,1)), date]]

delete_layout = [[Text("Delete score")],
                [user_delete_instance],
                [delete_instances_list],
                [Button("Delete")]]

workout_layout = [[Text("Workouts")],
                 [Text("Search workout picture:")],
                 [new_workout_picture]]

main_layout = [[ TabGroup([[ Tab("Search", Search_layout)],
                [Tab("New", Insert_layout)],
                [Tab("Delete", delete_layout)],
                [Tab("Workout", workout_layout)]])]]
#ready to delete window
delete_window_layout = [[Text("Are you sure you want to delete?")],
[Button("Yes"), Button("No")]]

window = Window("Highscores", main_layout)


while True:
    def update(user):
        scores = []
        for value in db[user].find():
            if value['exercise'] == '':
                insert_name = 'Empty'
            else:
                insert_name = '{} {} {} {}x{}'.format(value['exercise'], value['score'], value['unit'], value['sets'], value['reps'])
            scores.append(insert_name)
        window['Scoreboard'].Update(values= scores)
    event, values = window.read()
    if event in (None, 'exit'):
        break

    #new
    elif event == 'user_choice':
        update(scoreboard_user.get())
    elif event == 'calendar':
        date_string = calendar.get()
        show_new_date.update(date_string)

    elif event == 'Submit' and new_user.get() and new_exercise.get() and new_unit.get() and new_score.get() and new_set.get() and new_rep.get():
        db[new_user.get()].insert_one({'exercise': new_exercise.get(), 'score': float(new_score.get()), 'unit': new_unit.get(),  'sets': new_set.get(),  'reps': new_rep.get(),'date': calendar.get()})
        new_user.update('')
        new_exercise.update('')
        new_score.update('')
        new_unit.update('')
        new_rep.update('')
        new_set.update('')
        show_new_date.update('')
        
    elif event == 'Update':
        update(scoreboard_user.get())

    #Delete
    elif event == 'user_deletor':
        exercises = []
        for value in db[user_delete_instance.get()].find():
            if value['exercise'] == '':
                insert_name = 'Empty'
            else:
                insert_name = value['exercise']
            exercises.append(insert_name)
        window['delete_instance_list'].Update(values= exercises)

    elif event == 'Delete':
        delete_window = Window("Delete?", delete_window_layout)
        delete_event, delete_values = delete_window.read()
        if delete_event == 'Yes':
            db[user_delete_instance.get()].delete_one({'exercise': delete_instances_list.get()})
        delete_window.close()
        delete_instances_list.update('')

    elif event == "workout_picture":
        picture = new_workout_picture.get()
        sg.popup_get_text(message="write name:")

window.close()



