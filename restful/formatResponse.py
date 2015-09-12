def formatOutput(code, content={}):

    messages =  {
                    1000:"Lista de usuarios",
                    1001:"Datos del usuario",
                    1002:"El usuario no existe",
                    1003:"Nuevo usuario",
                   

                    2000:"Datos de la tabla y sus eventos",
                    2001:"Datos de la tabla pero sin eventos",
                    2002:"No hay tablas para esta fecha",
                    2003:"Datos de todas las tablas",
                    2004:"Error: el usuario no existe",
                    2005:"Nueva tabla dada de alta",
                    2006:"Error: la tabla ya existe",
                    2007:"Error: la tabla no existe",
                    2008:"Tabla actualizada correctamente",
                    

                }

    return {
            'code': code,
            'message': messages[code],
            'content':content
            }