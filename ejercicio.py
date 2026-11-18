from abc import ABC, abstractmethod
# Excepciones personalizadas
class ClienteInvalidoError(Exception):
    # Se lanza cuando los datos de un cliente no cumplen las validaciones.
    pass
class ServicioNoDisponibleError(Exception):
    # Se lanza cuando el servicio solicitado no esta disponible.
    pass
class ReservaInvalidaError(Exception):
    # Se lanza cuando una reserva contiene datos incorrectos o no cumple los requisitos.
    pass
class OperacionNoPermitidaError(Exception):
    # Se lanza cuando se intenta realizar una operacion que no esta permitida.
    pass
class DatosFaltantesError(Exception):
    # Se lanza cuando falta algun dato obligatorio para realizar una operacion.
    pass
class CalculoCostoError(Exception):
    # Se lanza cuando ocurre un error al calcular el costo de un servicio o reserva.
    pass

class Entidad(ABC):
    def __init__(self, id, fecha_creacion, estado):
        self.id = id
        self.fecha_creacion = fecha_creacion
        self.estado = estado

    @abstractmethod
    def validar(self):
        pass

    def mostrar_informacion(self):
        pass

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

class Cliente(Entidad):
    def __init__(self, id, fecha_creacion, estado,nombre, correo, telefono):

        super().__init__(id, fecha_creacion, estado)

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def validar(self):
        pass

    def validar_datos(self):
        pass

    def registrar_cliente(self):
        pass

    def actualizar_datos(self):
        pass

    def mostrar_informacion(self):
        pass

    def validar_correo(self):
        pass

    def validar_telefono(self):
        pass
class Servicio(Entidad):
    def __init__(self, id, fecha_creacion, estado,nombre, precio, disponibilidad):

        super().__init__(id, fecha_creacion, estado)

        self.nombre = nombre
        self.precio = precio
        self.disponibilidad = disponibilidad

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    def validar(self):
        pass

    def consultar_disponibilidad(self):
        pass
class ReservaSala(Servicio):
    def __init__(self, id, fecha_creacion, estado,nombre, precio, disponibilidad,capacidad, ubicacion):

        super().__init__(id, fecha_creacion, estado,nombre, precio, disponibilidad)

        self.capacidad = capacidad
        self.ubicacion = ubicacion

    def calcular_costo(self, duracion, descuento=0):
        pass

    def describir_servicio(self):
        pass

    def validar_parametros(self):
        pass

    def validar(self):
        pass
class AlquilerEquipo(Servicio):
    def __init__(self, id, fecha_creacion, estado,nombre, precio, disponibilidad,tipo_equipo, cantidad_disponible):

        super().__init__(id, fecha_creacion, estado,nombre, precio, disponibilidad)

        self.tipo_equipo = tipo_equipo
        self.cantidad_disponible = cantidad_disponible

    def calcular_costo(self, duracion, descuento=0):
        pass

    def describir_servicio(self):
        pass

    def validar_parametros(self):
        pass

    def validar(self):
        pass
class AsesoriaEspecializada(Servicio):
    def __init__(self, id, fecha_creacion, estado,nombre, precio, disponibilidad, especialidad, nombre_asesor, modalidad):

        super().__init__(id, fecha_creacion, estado,nombre, precio, disponibilidad)

        self.especialidad = especialidad
        self.nombre_asesor = nombre_asesor
        self.modalidad = modalidad

    def calcular_costo(self, duracion, descuento=0):
        pass

    def describir_servicio(self):
        pass

    def validar_parametros(self):
        pass

    def validar(self):
        pass
class Reserva:
    def __init__(self, id_reserva, cliente, servicio,
                 duracion, fecha, estado):

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.fecha = fecha
        self.estado = estado
        self.costo_total = 0

    def confirmar(self):
        pass

    def cancelar(self):
        pass

    def procesar(self):
        pass

    def calcular_total(self):
        pass

    def mostrar_reserva(self):
        pass
class GestorSistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        pass

    def buscar_cliente(self, id):
        pass

    def actualizar_cliente(self, id, datos):
        pass

    def eliminar_cliente(self, id):
        pass

    def registrar_servicio(self, servicio):
        pass

    def buscar_servicio(self, id):
        pass

    def eliminar_servicio(self, id):
        pass

    def crear_reserva(self, reserva):
        pass

    def buscar_reserva(self, id):
        pass

    def cancelar_reserva(self, id):
        pass

    def listar_clientes(self):
        pass

    def listar_servicios(self):
        pass

    def listar_reservas(self):
        pass
class ManejadorErrores:
    def __init__(self, archivo="software_fj.log"):
        self.archivo = archivo

    def registrar_error(self, error):
        pass

    def registrar_evento(self, mensaje):
        pass

