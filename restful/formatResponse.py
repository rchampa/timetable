def formatOutput(code, content={}):

    messages =  {
                    1000:"Lista de usuarios",
                    1001:"Datos del usuario",
                    1002:"El usuario no existe",
                    1003:"Nuevo usuario",
                   

                    2000:"",
                    2001:"",
                    

                }

    return {
            'code': code,
            'message': messages[code],
            'content':content
            }