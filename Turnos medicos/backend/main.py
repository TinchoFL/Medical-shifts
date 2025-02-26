from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Paciente, Doctor, CitaMedica
import datetime

app = Flask(__name__)
CORS(app)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://martin:martin@localhost:5432/tpintro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def hello_world():
    return 'Hello world!'


#Mostrar todos los pacientes
@app.route("/pacientes/", methods=["GET"])  
def pacientes():
    try:
        pacientes = Paciente.query.all()
        pacientes_data = []
        for paciente in pacientes:
            paciente_data = {
                'id': paciente.id,
                'nombre': paciente.nombre,
                'edad': paciente.edad,
                'genero': paciente.genero,
                'dni': paciente.dni          
            }
            pacientes_data.append(paciente_data)
        return jsonify(pacientes_data)
    except:
        return jsonify({"mensaje": "No hay pacientes registrados"})



# Mostrar un paciente
@app.route("/pacientes/<id_paciente>", methods=["GET"])
def paciente(id_paciente):
    try:
        paciente = Paciente.query.get(id_paciente)
        
        paciente_data = {
                'id': paciente.id,
                'nombre': paciente.nombre,
                'edad': paciente.edad,
                'genero': paciente.genero,
                'dni': paciente.dni
        }
        return jsonify(paciente_data)
    except:
        return jsonify("Error"), 404




#Crear Paciente
@app.route("/pacientes", methods=["POST"])
def crear_paciente():
    try:
        data = request.json
        nuevo_nombre = data.get('nombre') # saca del body el atributo nombre 
        nuevo_genero = data.get('genero')
        nueva_edad = data.get('edad')
        nuevo_dni = data.get('dni')
        nuevo_paciente = Paciente(nombre = nuevo_nombre, genero = nuevo_genero, edad = nueva_edad, dni = nuevo_dni) # crea una instancia de paciente
        db.session.add(nuevo_paciente) # agrega el paciente a la bdd
        db.session.commit()

        return jsonify({'paciente': {'id': nuevo_paciente.id, 
                                   'nombre': nuevo_paciente.nombre, 
                                   'genero': nuevo_paciente.genero,
                                   'edad': nuevo_paciente.edad,
                                   'dni': nuevo_paciente.dni }}), 201
    except:
        return jsonify({"mensaje": "No se pudo registrar el paciente"})








# Mostrar citas de un paciente
@app.route("/pacientes/<id_paciente>/citas", methods=["GET"])
def citas_de_paciente(id_paciente):
    try:
        #citas = CitaMedica.query.where(CitaMedica.id_paciente == id_paciente).all()
        
        citas = db.session.query(CitaMedica, Doctor).filter(CitaMedica.id_doctor == Doctor.id).filter(CitaMedica.id_paciente == id_paciente).all()

        citas_data = []
        for (cita, doctor) in citas:
            cita_data = {
                'id_cita': cita.id,
                'especialidad': doctor.especialidad,
                'doctor': doctor.nombre,
                'fecha_cita': cita.fecha_cita,
                'hora_cita': cita.hora_cita,           
            }
            citas_data.append(cita_data)
        return jsonify(citas_data)
    except:
        return jsonify({"mensaje": "No hay citas registradas"})




#Crear Cita medica
@app.route("/pacientes/<id_paciente>", methods=["POST"])
def crear_cita(id_paciente):
    try:
        # Validar y convertir datos
        nuevo_id_doctor = request.form.get("id_doctor")
        dia = request.form.get("dia")
        hora = request.form.get("hora")

        
        
        # Crear nueva cita
        nueva_cita = CitaMedica(
            id_paciente=id_paciente,
            id_doctor=nuevo_id_doctor,
            fecha_cita=dia,
            hora_cita=hora
            
        )

        # Agregar y confirmar la nueva cita en la base de datos
        db.session.add(nueva_cita)
        db.session.commit()

        return jsonify({'cita': {'id': nueva_cita.id }}), 201
    except Exception as error:
        print(error)
        return jsonify({"mensaje": "No se pudo registrar la cita"})



#Borrar Cita
@app.route("/citas/<id_cita>", methods=["DELETE"])
def eliminar_cita(id_cita):
    try:
        # Busca la cita médica por su ID
        cita = CitaMedica.query.get(id_cita)
        if cita is None:
            return jsonify({"mensaje": "Cita no encontrada"}), 404

        # Elimina la cita de la base de datos
        db.session.delete(cita)
        db.session.commit()

        return jsonify({"mensaje": "Cita eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": "Error al eliminar la cita"}), 500



#editar cita

@app.route("/pacientes/<id_cita>/<id_paciente>", methods=["PUT"])
def editar_cita(id_cita, id_paciente):
    try:
        # Validar y convertir datos
        nuevo_id_doctor = request.form.get("id_doctor")
        dia = request.form.get("dia")
        hora = request.form.get("hora")

        cita = CitaMedica.query.filter_by(id=id_cita).first()
        
        # Crear nueva cita
        cita.id = id_cita
        cita.id_paciente = id_paciente
        cita.id_doctor = nuevo_id_doctor
        cita.fecha_cita = dia
        cita.hora_cita = hora

        # Agregar y confirmar la nueva cita en la base de datos
        
        db.session.commit()

        return jsonify({'cita': {'id': nueva_cita.id }}), 201
    except Exception as error:
        print(error)
        return jsonify({"mensaje": "No se pudo registrar la cita"})





if __name__ == '__main__':
    print('Starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
    print('Started...')

