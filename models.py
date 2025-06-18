from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)

    # Relación con inventario (1 usuario puede tener muchos ítems)
    inventarios = db.relationship('Inventario', backref='usuario', lazy=True)


# Modelo Inventario
class Inventario(db.Model):
    __tablename__ = 'inventarios'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    vegetal = db.Column(db.String(80), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    consumido = db.Column(db.Boolean, nullable=False)

    @classmethod
    def obtener_por_usuario_no_consumidos(cls, id_usuario):
        return cls.query.filter_by(id_usuario=id_usuario, consumido=False).all()

    @classmethod
    def obtener_por_usuario_todos(cls, id_usuario):
        return cls.query.filter_by(id_usuario=id_usuario).all()

    @classmethod
    def crear(cls, id_usuario, vegetal, peso, dias, consumido=False):
        nuevo = cls(
            id_usuario=id_usuario,
            vegetal=vegetal,
            peso=peso,
            dias=dias,
            consumido=consumido
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo

    @classmethod
    def eliminar_por_id(cls, id_inventario):
        objeto = cls.query.get(id_inventario)
        if objeto:
            db.session.delete(objeto)
            db.session.commit()
            return True
        return False

    @classmethod
    def actualizar_consumido(cls, id_inventario, nuevo_estado):
        objeto = cls.query.get(id_inventario)
        if objeto:
            objeto.consumido = nuevo_estado
            db.session.commit()
            return objeto
        return None

    @classmethod
    def marcar_como_consumido_por_vegetal_y_peso(cls, id_usuario, vegetal, peso_objetivo):
        # Filtra los inventarios del usuario que coincidan con el vegetal y no hayan sido consumidos
        candidatos = cls.query.filter_by(id_usuario=id_usuario, vegetal=vegetal, consumido=False).all()

        if not candidatos:
            raise ValueError("El usuario no tiene el vegetal indicado sin consumir.")

        # Encuentra el objeto con peso más cercano al objetivo
        inventario_mas_cercano = min(candidatos, key=lambda x: abs(x.peso - peso_objetivo))

        # Marcar como consumido
        inventario_mas_cercano.consumido = True
        db.session.commit()

        return inventario_mas_cercano
