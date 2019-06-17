import os
import json
from datetime import datetime
import cherrypy
from models import RedisDb
from bse_script import GetEquityZip

class EquityApp(object):
    @cherrypy.expose
    def index(self):
        return open('views/index.html')

    @cherrypy.expose
    def get_top_equity(self, search=False):
        rdb = RedisDb()
        for_date = datetime.strptime(rdb.r_con.get('last_updated_date'), '%d%m%y').strftime('%d %B')
        if not search:
            return json.dumps({'top_10': rdb.get_top_entries(),'for_date': for_date})
        return json.dumps({'top_10': rdb.seach_for_name(search),'for_date': for_date})

    @cherrypy.expose
    def refresh(self, for_date):
        for_date = datetime.strptime(for_date, '%Y-%m-%d').strftime('%d%m%y')
        get_zip = GetEquityZip(for_date=for_date)
        rdb = get_zip.red
        if for_date == rdb.r_con.get('last_updated_date'):
            return False
        res = get_zip.get_zip_from_bse()
        if res['success']:
            for_date = datetime.strptime(rdb.r_con.get('last_updated_date'), '%d%m%y').strftime('%d %B')
            return json.dumps({'top_10': rdb.get_top_entries(),'for_date': for_date})
        return False

if __name__ == '__main__':
    config = {
        '/': {
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/assests': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'assests'
        }
    }
    # import pdb; pdb.set_trace()
    cherrypy.quickstart(EquityApp(),config=config)
