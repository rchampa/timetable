#!/usr/bin/python

from flaskapp import app as application

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 5000, application)
    # Wait for a single request, serve it and quit.
    #httpd.handle_request()
    httpd.serve_forever()



# #
# # Below for testing only
# #
# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     httpd = make_server('localhost', 8051, application)
#     # Wait for a single request, serve it and quit.
#     httpd.handle_request()
