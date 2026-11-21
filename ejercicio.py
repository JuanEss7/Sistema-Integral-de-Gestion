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
class ManejadorErrores:
    def __init__(self, archivo="errores.log"):
        self.archivo = archivo

    def registrar_error(self, error):
        try:
            with open(self.archivo, "a", encoding="utf-8") as archivo:
                archivo.write(
                    f"{datetime.now()} | ERROR | "
                    f"{type(error).__name__}: {error}\n"
                )
        except OSError:
            print("No fue posible escribir el error en el archivo de log.")

    def registrar_evento(self, mensaje):
        try:
            with open(self.archivo, "a", encoding="utf-8") as archivo:
                archivo.write(
                    f"{datetime.now()} | EVENTO | {mensaje}\n"
                )
        except OSError:
            print("No fue posible escribir el evento en el archivo de log.")

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
        self.validar()
        LOG.registrar_evento(
            f"Cliente {self.id} - {self.nombre} registrado."
        )
        return True
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
        LOG.registrar_evento(f"Cliente {self.id} actualizado.")
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
    def __init__(self, id, fecha_creacion=None, estado="Activo",nombre=None, precio=None, disponibilidad=True,capacidad=None, ubicacion=None):

        super().__init__(id, fecha_creacion, estado,nombre, precio, disponibilidad)

        self.capacidad = capacidad
        self.ubicacion = ubicacion
        self.validar()

    def validar_parametros(self):
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero positivo.")

        if not isinstance(self.ubicacion, str) or self.ubicacion.strip() == "":
            raise DatosFaltantesError("La ubicacion es obligatoria.")
        
    def describir_servicio(self):
        return (
            f"Sala: {self.nombre}. Capacidad: {self.capacidad} personas. "
            f"Ubicacion: {self.ubicacion}. Precio por hora: ${self.precio}."
        )
class AlquilerEquipo(Servicio):
    def __init__(self, id, fecha_creacion=None, estado="Activo",nombre=None, precio=None, disponibilidad=True,tipo_equipo=None, cantidad_disponible=None):

        super().__init__(id, fecha_creacion, estado,nombre, precio, disponibilidad)

        self.tipo_equipo = tipo_equipo
        self.cantidad_disponible = cantidad_disponible
        self.validar()

    def describir_servicio(self):
        return (
            f"Equipo: {self.nombre}. Tipo: {self.tipo_equipo}. "
            f"Cantidad disponible: {self.cantidad_disponible}. "
            f"Precio por dia: ${self.precio}."
        )

    def validar_parametros(self):
        if not isinstance(self.tipo_equipo, str) or self.tipo_equipo.strip() == "":
            raise DatosFaltantesError("El tipo de equipo es obligatorio.")

        if not isinstance(self.cantidad_disponible, int) or self.cantidad_disponible < 0:
            raise ValueError(
                "La cantidad disponible debe ser un entero igual o mayor que cero."
            )
    def consultar_disponibilidad(self):
        return (
            super().consultar_disponibilidad()
            and self.cantidad_disponible > 0
        )
    
class AsesoriaEspecializada(Servicio):
    def __init__(self, id, fecha_creacion=None, estado="Activo",nombre=None, precio=None, disponibilidad=True,especialidad=None, nombre_asesor=None, modalidad=None):

        super().__init__(id, fecha_creacion, estado,nombre, precio, disponibilidad)

        self.especialidad = especialidad
        self.nombre_asesor = nombre_asesor
        self.modalidad = modalidad
        self.validar()

    def describir_servicio(self):
        return (
            f"Asesoria: {self.nombre}. Especialidad: {self.especialidad}. "
            f"Asesor: {self.nombre_asesor}. Modalidad: {self.modalidad}. "
            f"Precio por hora: ${self.precio}."
        )

    def validar_parametros(self):
        if not isinstance(self.especialidad, str) or self.especialidad.strip() == "":
            raise DatosFaltantesError("La especialidad es obligatoria.")

        if not isinstance(self.nombre_asesor, str) or self.nombre_asesor.strip() == "":
            raise DatosFaltantesError("El nombre del asesor es obligatorio.")

        if self.modalidad not in ("Virtual", "Presencial"):
            raise ValueError("La modalidad debe ser Virtual o Presencial.")


class Reserva:
    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")
    def __init__(self, id_reserva, cliente, servicio, duracion, fecha, estado=ESTADOS_VALIDOS[0], cantidad = 1):
        if id_reserva is None or type(id_reserva) != str or id_reserva.strip() == "":
            raise DatosFaltantesError("El ID de la reserva es obligatorio.")
        
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.fecha = fecha
        self.estado = estado
        self.cantidad = cantidad
        self.costo_total = 0
        self.recursos_asignados = False
        self.validar()

    def validar(self):
        if not isinstance(self.cliente, Cliente):
            raise ReservaInvalidaError("Debe seleccionar un cliente valido.")

        if not isinstance(self.servicio, Servicio):
            raise ReservaInvalidaError("Debe seleccionar un servicio valido.")

        self.cliente.validar()
        self.servicio.validar()

        if self.cliente.estado != "Activo":
            raise ReservaInvalidaError("No se pueden crear reservas para clientes inactivos.")

        if not isinstance(self.duracion, (int, float)) or self.duracion <= 0:
            raise ReservaInvalidaError("La duracion debe ser mayor que cero.")

        if not isinstance(self.cantidad, int) or self.cantidad <= 0:
            raise ReservaInvalidaError("La cantidad debe ser un entero mayor que cero.")

        if self.estado not in self.ESTADOS_VALIDOS:
            raise ReservaInvalidaError("El estado de la reserva no es valido.")

        if self.fecha is None or str(self.fecha).strip() == "":
            raise DatosFaltantesError("La fecha de la reserva es obligatoria.")

        return True

    def procesar(self):
        if self.estado != self.ESTADOS_VALIDOS[1]:
            raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas.")

        # Se libera el recurso al terminar el servicio.
        if self.recursos_asignados:
            if isinstance(self.servicio, AlquilerEquipo):
                self.servicio.disponibilidad = (self.servicio.cantidad_disponible > 0)
            else:
                self.servicio.disponibilidad = True

        self.recursos_asignados = False
        self.estado = self.ESTADOS_VALIDOS[3]
        LOG.registrar_evento(f"Reserva {self.id_reserva} procesada.")
        return True
    
    def cancelar(self):
        if self.estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitidaError("La reserva no se puede cancelar en su estado actual.")

        if self.estado == self.ESTADOS_VALIDOS[1] and self.recursos_asignados:
            if isinstance(self.servicio, AlquilerEquipo):
                self.servicio.cantidad_disponible += self.cantidad
            self.servicio.disponibilidad = True

        self.recursos_asignados = False
        self.estado = self.ESTADOS_VALIDOS[2]
        return True

    
    def confirmar(self):
        if self.estado != self.ESTADOS_VALIDOS[0]:
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")

        if not self.servicio.consultar_disponibilidad():
            raise ServicioNoDisponibleError(f"El servicio {self.servicio.nombre} no esta disponible.")

        if isinstance(self.servicio, AlquilerEquipo):
            if self.servicio.cantidad_disponible < self.cantidad:
                raise ServicioNoDisponibleError("No hay suficientes unidades del equipo.")

            self.servicio.cantidad_disponible -= self.cantidad

            if self.servicio.cantidad_disponible == 0:
                self.servicio.disponibilidad = False

        else:
            self.servicio.disponibilidad = False

        self.recursos_asignados = True
        self.estado = self.ESTADOS_VALIDOS[1]
        return True



    def calcular_total(self,descuento=0, impuesto=0):
        try:
            costo = self.servicio.calcular_costo(self.duracion, descuento, impuesto)
            self.costo_total = round(costo * self.cantidad, 2)

        except Exception as error:
            LOG.registrar_error(error)
            raise CalculoCostoError("No fue posible calcular el costo de la reserva.") from error

        else:
            return self.costo_total
        finally:
            LOG.registrar_evento(
                f"Se intento calcular el costo de la reserva {self.id_reserva}."
            )

    def mostrar_reserva(self):
        return (
            f"Reserva: {self.id_reserva} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Fecha: {self.fecha} | "
            f"Duracion: {self.duracion} | Cantidad: {self.cantidad} | "
            f"Estado: {self.estado} | Total: ${self.costo_total}"
        )



class GestorSistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.log = LOG
        self.log.registrar_evento("Sistema Software FJ iniciado.")

    def registrar_cliente(self, cliente):
        try:
            if not isinstance(cliente, Cliente):
                raise ClienteInvalidoError("El objeto no es un cliente.")

            cliente.validar()

            if self.buscar_cliente(cliente.id) is not None:
                raise OperacionNoPermitidaError("Ya existe un cliente con ese ID.")

            self.clientes.append(cliente)
            cliente.registrar_cliente()
            return cliente

        except Exception as error:
            self.log.registrar_error(error)
            raise

    def buscar_cliente(self, id):
        for cliente in self.clientes:
            if cliente.id == str(id):
                return cliente
        return None

    def actualizar_cliente(self, id, datos):
        cliente = self.buscar_cliente(id)

        if cliente is None:
            raise ClienteInvalidoError("No se encontro el cliente.")

        if not isinstance(datos, dict):
            raise ValueError("Los datos deben enviarse en un diccionario.")

        try:
            cliente.actualizar_datos(
                nombre=datos.get("nombre"),
                correo=datos.get("correo"),
                telefono=datos.get("telefono")
            )
            return cliente

        except Exception as error:
            self.log.registrar_error(error)
            raise

    def eliminar_cliente(self, id):
        cliente = self.buscar_cliente(id)

        if cliente is None:
            raise ClienteInvalidoError("No se encontro el cliente.")

        for reserva in self.reservas:
            if reserva.cliente.id == cliente.id and reserva.estado in ("Pendiente", "Confirmada"):
                raise OperacionNoPermitidaError("El cliente tiene reservas activas.")

        self.clientes.remove(cliente)
        self.log.registrar_evento(f"Cliente {id} eliminado.")
        return True

    def buscar_servicio(self, id):
        for servicio in self.servicios:
            if servicio.id == str(id):
                return servicio
        return None
    def registrar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise ValueError("El objeto no es un servicio valido.")

            servicio.validar()

            if self.buscar_servicio(servicio.id) is not None:
                raise OperacionNoPermitidaError("Ya existe un servicio con ese ID." )

            self.servicios.append(servicio)
            self.log.registrar_evento(f"Servicio {servicio.id} registrado.")
            return servicio

        except Exception as error:
            self.log.registrar_error(error)
            raise


    def eliminar_servicio(self, id):
        servicio = self.buscar_servicio(id)

        if servicio is None:
            raise ServicioNoDisponibleError("No se encontro el servicio.")

        for reserva in self.reservas:
            if reserva.servicio.id == servicio.id and reserva.estado in ("Pendiente", "Confirmada"):
                raise OperacionNoPermitidaError("El servicio tiene reservas activas.")

        self.servicios.remove(servicio)
        self.log.registrar_evento(f"Servicio {id} eliminado.")
        return True

    def buscar_reserva(self, id):
        for reserva in self.reservas:
            if reserva.id_reserva == str(id):
                return reserva
        return None
    
    def crear_reserva(self, reserva):
        try:
            if not isinstance(reserva, Reserva):
                raise ReservaInvalidaError("El objeto no es una reserva.")

            reserva.validar()

            if self.buscar_cliente(reserva.cliente.id) is None:
                raise ReservaInvalidaError("El cliente no esta registrado en el sistema.")

            if self.buscar_servicio(reserva.servicio.id) is None:
                raise ReservaInvalidaError("El servicio no esta registrado en el sistema.")

            if self.buscar_reserva(reserva.id_reserva) is not None:
                raise OperacionNoPermitidaError("Ya existe una reserva con ese ID.")

            self.reservas.append(reserva)
            self.log.registrar_evento(f"Reserva {reserva.id_reserva} creada.")
            return reserva

        except Exception as error:
            self.log.registrar_error(error)
            raise
    def confirmar_reserva(self, id):
        reserva = self.buscar_reserva(id)

        if reserva is None:
            raise ReservaInvalidaError("No se encontro la reserva.")

        try:
            reserva.confirmar()
            return reserva
        except Exception as error:
            self.log.registrar_error(error)
            raise

    def procesar_reserva(self, id):
        reserva = self.buscar_reserva(id)
        if reserva is None:
            raise ReservaInvalidaError("No se encontro la reserva.")
        try:
            reserva.procesar()
            return reserva
        except Exception as error:
            self.log.registrar_error(error)
            raise

    def cancelar_reserva(self, id):
        reserva = self.buscar_reserva(id)

        if reserva is None:
            raise ReservaInvalidaError("No se encontro la reserva.")

        try:
            reserva.cancelar()
            return reserva
        except Exception as error:
            self.log.registrar_error(error)
            raise

    def listar_clientes(self):
        return self.clientes.copy()

    def listar_servicios(self):
        return self.servicios.copy()

    def listar_reservas(self):
        return self.reservas.copy()
    
LOG = ManejadorErrores()


