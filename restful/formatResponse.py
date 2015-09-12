def formatOutput(code, content={}):

    messages =  {
                    1000:"Lista de usuarios",
                    1001:"Datos del usuario",
                    1002:"El usuario no existe",
                    1003:"Nuevo usuario",
                   

                    2000:"Datos de la tabla y sus eventos",
                    2001:"Datos de la tabla pero sin eventos",
                    2002:"No hay tablas para esta fecha",
                    

                }

    return {
            'code': code,
            'message': messages[code],
            'content':content
            }