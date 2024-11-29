from flask import Flask, render_template, redirect, url_for, request
from models import db, Tarea
from sqlalchemy import text
from routes.auth_utils import *  # Autenticador
from app import app

########################################## Dashboard de Tareas ##############################################
@app.route('/dashboard', methods=['GET'])
@login_required
@role_required(['Empleado', 'Administrador'])
def dashboard():
    # Contar las tareas en cada estado
    tareas_pendientes_count = Tarea.query.filter_by(estado='Pendiente').count()
    tareas_en_progreso_count = Tarea.query.filter_by(estado='En Progreso').count()
    tareas_completadas_count = Tarea.query.filter_by(estado='Completada').count()

    # Pasar los conteos al template
    return render_template("/panel/dashboard.html", active_page='dashboard',
                           tareas_pendientes_count=tareas_pendientes_count,
                           tareas_en_progreso_count=tareas_en_progreso_count,
                           tareas_completadas_count=tareas_completadas_count)
