from abc import abstractmethod, ABC
from .Util import getItemBy


class Base(ABC):
    """
        Clase base para la implementacion de los tipos
        Worker y Fork
    """

    Topico = ''

    def __init__(self, Topico):
        self.Topico = Topico

    @abstractmethod
    def process(self, span, request, fnc, params=[]):
        """
            Metodo que se encargara de procesar los mensajes
            que se enviaran al microservicio.
        """
        return 0

    def confForks(self, conf):
        """
            Metodo para registrar la configuracion del metodo
            que se ejecutara.
        """
        pass

    def formatResponse(self, original, resp, errorCode=0, errorWorker=None):
        """
            Metodo que se encarga de darle formato a la
            salida del procesamiento de la accion.
        """

        errorCodeBk = None

        try:
            errorCodeBk = errorCode
            # Prevenir el paso de string como error
            errorCode = int(errorCode)
        except Exception:
            print(
                'Ocurrio une error al realizar el CAST del error: {}'.format(
                    errorCodeBk
                )
            )
            errorCode = -99

        # Regresar la respuesta con el formato correcto
        if errorWorker is not None:
            pass

        resp = {
            "errorCode": errorCode,
            "response": {
                "data": original.get("data", None),
                "headers": original.get("headers", {}),
                "metadata": original.get("metadata", {}),
                "response": {
                    "data": {
                        "response": resp
                    },
                    "meta": {
                        "id_transaction": original["metadata"]["id_transaction"],
                        "status": 'ERROR' if errorCode < 0 or errorCode > 0 else 'SUCCESS'
                    }
                },
                "uuid": original.get("uuid", None),
            },
            "errorWorker": errorWorker
        }

        # Retornar los datos
        return resp

    def getParams(self, data, paramList):
        """
            Metodo para recuperar los datos segun la configuracion
            de los parametros.
        """
        # Parametros
        paramsInject = {}

        # Seleccion de parametros
        for i in paramList:
            if i == 'data':
                paramsInject.update({i: data.get('data')})
            elif i == 'filters':
                data_params = self.__transformFilter(
                    getItemBy('metadata.filters', data))
                data_params = {} if data_params is None else data_params
                paramsInject.update({
                    i: data_params,
                })
            elif i == 'authorizacion':
                paramsInject.update({i: data["headers"]["Authorizacion"]})
            elif i == 'uuid':
                paramsInject.update({i: getItemBy('metadata.uuid', data)})
            elif i == 'response':
                paramsInject.update(
                    {i: getItemBy('response.data.response', data)})

        return paramsInject

    def __transformFilter(self, data):
        """
            Metodo para dar un forma coherente a los filtros
        """
        resp = {}
        # Validar que existan datos
        if data is None:
            return data

        for k in data:
            l = data.get(k)
            if len(l) == 1:
                if len(l[0].split(',')) > 1:
                    resp.update({k: l[0].split(',')})
                else:
                    resp.update({k: l[0]})
            else:
                resp.update({k: l})

        return resp
