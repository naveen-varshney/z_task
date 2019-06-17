import random
import string
import os
import cherrypy
from models import RedisDb

class EquityApp(object):
    @cherrypy.expose
    def index(self):
        return open('views/index.html')

    @cherrypy.expose
    def get_top_equity(self, length=8):
        rdb = RedisDb()
        return rdb.get_top_entries()


if __name__ == '__main__':
    config = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/assests': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '/assests'
        }
    }
    # import pdb; pdb.set_trace()
    cherrypy.quickstart(EquityApp(),config=config)
