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
        try:
            rdb = RedisDb()
            for_date = datetime.strptime(rdb.r_con.get('last_updated_date'), '%d%m%y').strftime('%d %B')
            cherrypy.log('get_top_equity called for date {}'.format(for_date))
            if not search:
                return json.dumps({'success': True,'top_10': rdb.get_top_entries(),'for_date': for_date})
            return json.dumps({'success': True,'top_10': rdb.seach_for_name(search),'for_date': for_date})
        except Exception as e:
            cherrypy.log('get_top_equity error occured',traceback=True)
        return json.dumps({'success': False})

    @cherrypy.expose
    def refresh(self, for_date):
        try:
            for_date = datetime.strptime(for_date, '%Y-%m-%d').strftime('%d%m%y')
            cherrypy.log('get_top_equity called for date {}'.format(for_date))
            get_zip = GetEquityZip(for_date=for_date)
            rdb = get_zip.red
            if for_date == rdb.r_con.get('last_updated_date'):
                return json.dumps({'success': True,'top_10': rdb.get_top_entries(),'for_date': for_date})
            res = get_zip.get_zip_from_bse()
            if res['success']:
                for_date = datetime.strptime(rdb.r_con.get('last_updated_date'), '%d%m%y').strftime('%d %B')
                return json.dumps({'success': True,'top_10': rdb.get_top_entries(),'for_date': for_date})
            return json.dumps({'success': False,'message':res.get('message',"Something went wrong")})
        except Exception as e:
            cherrypy.log('refresh error occured',traceback=True)
        return json.dumps({'success': False})

if __name__ == '__main__':
    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000)),
	    'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/': {
            'log.access_file': '',
            'log.error_file': 'error_file.log'
        },
        '/assests': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'assests'
        },

         '/favicon.ico':
         {
             'tools.staticfile.on': True,
             'tools.staticfile.filename': 'favicon.ico'
         }
    }
    # import pdb; pdb.set_trace()
    cherrypy.quickstart(EquityApp(),config=config)
