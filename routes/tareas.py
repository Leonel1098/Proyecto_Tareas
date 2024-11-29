from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import db, Tarea, Empleado
from routes.auth_utils import *  # Autenticador
from sqlalchemy import text
from config import socketio
from app import app

@app.route('/tareas', methods=['GET', 'POST'])
@login_required
@role_required(['Empleado', 'Administrador'])
def tareas():
    if request.method == 'POST':
        # Obtener los datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        asignadaA = request.form['asignadaA']

        # Crear una nueva tarea
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            estado=estado,
            asignadaA=asignadaA
        )

        # Guardar la tarea en la base de datos
        db.session.add(nueva_tarea)
        db.session.commit()

        # Emitir evento WebSocket para notificar a todos los usuarios
        socketio.emit('tarea_creada', {
            'mensaje': f'Nueva tarea "{titulo}" creada con éxito',
            'tareaID': nueva_tarea.tareaID,
            'titulo': nueva_tarea.titulo,
            'descripcion': nueva_tarea.descripcion,
            'estado': nueva_tarea.estado,
            'asignadaA': nueva_tarea.asignadaA
        })

        # Redirigir a la lista de tareas
        return redirect(url_for('tareas'))

    # Filtros para estado y búsqueda por nombreEmpleado
    estado_filtro = request.args.get('estado')
    nombre_empleado = request.args.get('nombreEmpleado')
    query = Tarea.query

    # Filtrar por estado si está definido y no es "Todos"
    if estado_filtro and estado_filtro != 'Todos':
        query = query.filter_by(estado=estado_filtro)

    # Filtrar por nombreEmpleado si está definido
    if nombre_empleado:
        query = query.join(Empleado).filter(Empleado.nombreEmpleado.ilike(f"%{nombre_empleado}%"))

    # Obtener las tareas filtradas
    tareas = query.all()

    # Obtener la lista de empleados para el formulario
    empleados = Empleado.query.all()

    return render_template(
        '/tareas/tareas.html',
        active_page='tareas',
        tareas=tareas,
        empleados=empleados
    )


########################################## Cargar datos y editar tarea ##############################################
@app.route('/tarea/<int:tareaID>/editar', methods=['GET'])
def cargarTareaEditar(tareaID):
    tarea = Tarea.query.get_or_404(tareaID)
    return jsonify({
        'tareaID': tarea.tareaID,
        'titulo': tarea.titulo,
        'descripcion': tarea.descripcion,
        'estado': tarea.estado,
        'asignadaA': tarea.asignadaA
    })

@app.route('/editarTarea', methods=['POST'])
def editarTarea():
    tareaID = request.form['tareaID']
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    estado = request.form['estado']
    asignadaA = request.form['asignadaA']
    
    tarea = Tarea.query.get_or_404(tareaID)
    tarea.titulo = titulo
    tarea.descripcion = descripcion
    tarea.estado = estado
    tarea.asignadaA = asignadaA

    db.session.commit()
    return redirect(url_for('tareas'))  # Redirigir a la lista de tareas después de guardar

########################################## Eliminar Tarea ##############################################
@app.route('/eliminarTarea/<int:tareaID>', methods=['GET'])
def eliminarTarea(tareaID):
    # Buscar la empresa en la base de datos
    tarea = Tarea.query.get(tareaID)
    
    if tarea:
        tarea_info = {
            'tareaID': tarea.tareaID,
            'titulo': tarea.titulo
        }
        db.session.delete(tarea)
        db.session.commit()
    
     # Emitir evento para notificar a todos los clientes
    socketio.emit('tarea_eliminada', {'mensaje': f'Tarea con ID {tareaID} eliminada con éxito'})
    return redirect(url_for('tareas'))