import json

from server_multijugador.comunication.states import STATE_GAME


class PlayerDTO:
    def __init__(self, identificacion, name, velocidad, posicion, puesto):
        self.id = identificacion
        self.vel = velocidad
        self.position = posicion
        self.name = name
        self.puesto = puesto

    def to_dict(self):
        return {
            'id': self.id,
            'vel': self.vel,
            'position': self.position,
            'name': self.name,
            'puesto': self.puesto
        }


class ComunicationDTO:
    def __init__(self, estado, mensaje):
        self.state = estado.name
        self.msg = mensaje

    def to_dict(self):
        return {
            'state': self.state,
            'msg': self.msg
        }


def createMensaje(state: STATE_GAME, msg):
    dto = ComunicationDTO(state, msg).to_dict()
    return json.dumps(dto)
