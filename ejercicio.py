from abc import ABC, abstractmethod
from datetime import datetime
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
    def __init__(self, id, fecha_creacion = None, estado="Activo"):
        if id is None or str(id).strip() == "":
            raise DatosFaltantesError("El ID es obligatorio.")

        self.id = str(id)
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.estado = estado

    @abstractmethod
    def validar(self):
        pass

    def mostrar_informacion(self):
        return (
            f"ID: {self.id} | Fecha: {self.fecha_creacion} | "
            f"Estado: {self.estado}"
        )

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado is None or len(nuevo_estado) == 0 or nuevo_estado not in ("Activo","Inactivo"):
            raise DatosFaltantesError("Debe indicar el nuevo estado.")
        self.estado = nuevo_estado

class Cliente(Entidad):
    def __init__(self, id, fecha_creacion=None, estado="Activo", nombre=None, correo=None, telefono=None):
        super().__init__(id, fecha_creacion, estado)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar()
# Metodo encargado de validar los datos del cliente
    def validar(self):
        # Validando que el nombre sea texto
        if not isinstance(self.nombre, str) or len(self.nombre.strip()) < 2:
            raise ClienteInvalidoError("El nombre debe tener al menos dos caracteres.")
        self.validar_correo()
        self.validar_telefono()
        if self.estado not in ("Activo", "Inactivo"):
            raise ClienteInvalidoError("El estado debe ser Activo o Inactivo.")
        return True

    def registrar_cliente(self):
        pass
# Metodo encargado de actualizar los datos del cliente
    def actualizar_datos(self, nombre=None, correo=None, telefono=None):
        # Guardamos los datos anteriores por si los nuevos son incorrectos.
        nombre_anterior = self.nombre
        correo_anterior = self.correo
        telefono_anterior = self.telefono
        #Actulizando datos
        if nombre is not None:
            self.nombre = nombre
        if correo is not None:
            self.correo = correo
        if telefono is not None:
            self.telefono = telefono
        try:
            self.validar()
        except Exception:
            # Actualizamos los datos con los valores anteriores y lanzamos la misma excepcion
            self.nombre = nombre_anterior
            self.correo = correo_anterior
            self.telefono = telefono_anterior
            raise
        return True
# Metodo encargado de mostrar la informacion registrada del cliente
    def mostrar_informacion(self):
        return (
            f"{super().mostrar_informacion()} | Nombre: {self.nombre} | "
            f"Correo: {self.correo} | Telefono: {self.telefono}"
        )
# Metodo encargado de validar el correo
    def validar_correo(self):
        # Validando que el correo sea texto
        if not isinstance(self.correo, str):
            raise ClienteInvalidoError("El correo debe ser texto.")
        # Validando el correo
        if "@" not in self.correo or "." not in self.correo:
            raise ClienteInvalidoError("El correo electronico no es valido.")

        if self.correo.startswith("@") or self.correo.endswith("@"):
            raise ClienteInvalidoError("El correo electronico no es valido.")
        return True
# Metodo encargado de validar el telefono
    def validar_telefono(self):
        # Validando que el telefono sea texto
        if self.telefono is None or not isinstance(self.telefono, str) or self.telefono == "":
            raise DatosFaltantesError("El telefono es obligatorio.")
        # Validando que sean digitos 
        cantidad_digitos = 0
        for caracter in self.telefono:
            if caracter.isdigit():
                cantidad_digitos += 1
        # Validando la longitud
        if cantidad_digitos < 7 or cantidad_digitos > 15:
            raise ClienteInvalidoError("El telefono debe tener entre 7 y 15 digitos.")
        return True
    
class Servicio(Entidad):
    def __init__(self, id, fecha_creacion=None, estado="Activo",nombre=None, precio=None, disponibilidad=None):
        super().__init__(id, fecha_creacion, estado)
        self.nombre = nombre
        self.precio = precio
        self.disponibilidad = disponibilidad

    
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise CalculoCostoError("La duracion debe ser mayor que cero.")

        if not isinstance(descuento, (int, float)) or descuento < 0 or descuento > 100:
            raise CalculoCostoError("El descuento debe estar entre 0 y 100.")

        if not isinstance(impuesto, (int, float)) or impuesto < 0 or impuesto > 100:
            raise CalculoCostoError("El impuesto debe estar entre 0 y 100.")
        
        subtotal = self.precio * duracion
        valor_descuento = subtotal * descuento / 100
        subtotal = subtotal - valor_descuento
        total = subtotal + (subtotal * impuesto / 100)

        return round(total, 2)

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    def validar(self):
        if not isinstance(self.nombre, str) or self.nombre.strip() == "":
            raise DatosFaltantesError("El nombre del servicio es obligatorio.")

        if not isinstance(self.precio, (int, float)) or self.precio <= 0:
            raise CalculoCostoError("El precio debe ser un numero mayor que cero.")

        if self.estado not in ("Activo", "Inactivo"):
            raise OperacionNoPermitidaError("El estado del servicio no es valido.")

        if not isinstance(self.disponibilidad, bool):
            raise ValueError("La disponibilidad debe ser True o False.")
        self.validar_parametros()
        return True

    def consultar_disponibilidad(self):
        return self.disponibilidad and self.estado == "Activo"
    
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

