from flask import Blueprint, render_template, request, flash , jsonify, Response
from flask_login import current_user, login_required
from .models import Note, Project
from . import db
import json
import time
import datetime
import smtplib

total_seconds=0

views = Blueprint('views',__name__)

@views.route('/',methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('Title')
        genre = request.form.get('Genre')
        type = request.form.get('Type')
        description = request.form.get('Description')
        project = Project(project_name=title,genre=genre,project_type=type,description=description,user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        # sender = "cristinastegaru89@yahoo.com"
        # receiver = current_user.email
        # print(receiver)
        # message = "New project added"
        # smtpObj = smtplib.SMTP('localhost')
        # smtpObj.sendmail(sender, receiver, message)         
        # print ("Successfully sent email")

    return render_template("projects.html",user=current_user)

   
@views.route('/notes',methods=['GET', 'POST'])
@login_required
def notes():
     if request.method == 'POST':
        note = request.form.get('note')
        new_note = Note(content=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')

     return render_template("notes.html",user=current_user)

@views.route('/delete-project', methods=['POST'])
def delete_project():
    projects = json.loads(request.data)
    projectId = projects['projectId']
    projects = Project.query.get(projectId)
    if projects:
        if projects.user_id == current_user.id:
            db.session.delete(projects)
            db.session.commit()

    return jsonify({})

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/sprint',methods=['GET', 'POST'])
@login_required
def sprint():
    timer="00:00"
    if request.method == 'POST':
        ore= int(request.form.get("Hours"))
        minute= int(request.form.get("Minutes"))
        # secunde= int(request.form.get("Seconds"))
        global total_seconds
        total_seconds = ore * 3600 + minute * 60 
    if total_seconds >= 0:
        timer = str(datetime.timedelta(seconds = total_seconds))
        total_seconds -= 60
    split_timer= timer.split(":")[0] + ":" + timer.split(":")[1]
    return render_template("sprint.html",user=current_user,value=split_timer)


# @views.route('/countdown', methods=['GET'])
# def countdown():
#     global total_seconds 
#     if total_seconds >= 0:
#         timer = datetime.timedelta(seconds = total_seconds)
#         print(timer, end="\r")
#         total_seconds -= 1
#         return """<meta http-equiv="refresh" content="1" /> {}.""".format(timer)
#     else:
#         time.sleep(5)
    
 
    

@views.route('/character_template')
@login_required
def character_template():
    return render_template("character_template.html",user=current_user)

@views.route('/progress')
@login_required
def progress():
    return render_template("progress.html",user=current_user)