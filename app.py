import random
import string
import cherrypy

class EquityApp(object):
    @cherrypy.expose
    def index(self):
        return open('views/index.html')

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))


if __name__ == '__main__':
    cherrypy.quickstart(EquityApp())
