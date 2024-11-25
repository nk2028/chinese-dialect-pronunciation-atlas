import cherrypy
import csv
import json
import sqlite3

def 構建():
    是方言的簡稱們 = set()
    簡稱到分區與顏色 = {}
    簡稱到排序 = {}

    with open('data/info.csv', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"', strict=True)

        _, _, *rest = next(reader)
        分區_idx = rest.index('地圖集二分區')
        顏色_idx = rest.index('地圖集二顏色')
        排序_idx = rest.index('地圖集二排序')

        for _, 簡稱, *rest in reader:
            分區 = rest[分區_idx]
            顏色 = rest[顏色_idx]
            排序 = rest[排序_idx]

            if 分區 and 顏色 and 排序:
                是方言的簡稱們.add(簡稱)
                簡稱到分區與顏色[簡稱] = 分區, 顏色
                簡稱到排序[簡稱] = 排序

    return 是方言的簡稱們, 簡稱到分區與顏色, 簡稱到排序

是方言的簡稱們, 簡稱到分區與顏色, 簡稱到排序 = 構建()

class Server:
    def __init__(self):
        self.db = sqlite3.connect('file:data/mcpdict.db?mode=ro', uri=True, check_same_thread=False)  # we are safe because we only use the database in a read-only manner

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('https://nk2028.shn.hk/hdqt/')

    @cherrypy.expose
    def default(self, *args, **kwargs):
        message = {'錯誤': '請求的資源不存在'}
        cherrypy.response.status = 404
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Credentials'] = 'true'
        return json.dumps(message, ensure_ascii=False)

    @cherrypy.expose
    def query(self, string: str) -> dict:
        if not string:
            return []

        cur = self.db.cursor()

        string = list({漢字: None for 漢字 in string})  # 去重
        placeholders = ', '.join('?' for _ in string)
        cur.execute(f'SELECT * FROM "mcpdict" WHERE "漢字" IN ({placeholders});', string)

        results = cur.fetchall()
        column_names = [description[0] for description in cur.description]

        cur.close()

        漢字到idx = {漢字: idx for idx, 漢字 in enumerate(string)}

        漢字_column = column_names.index('漢字')
        results = sorted(results, key=lambda result: 漢字到idx[result[漢字_column]])
        字頭們 = [result[漢字_column] for result in results]

        res = [('', *字頭們)] + sorted(
            ((
                簡稱, *簡稱到分區與顏色[簡稱], *[字音 or '' for 字音 in 字音們])
                for 簡稱, *字音們
                in zip(column_names, *results)
                if 簡稱 in 是方言的簡稱們 and any(字音 for 字音 in 字音們)
            ),
            key=lambda 簡稱_rest: 簡稱到排序[簡稱_rest[0]]
        )

        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Credentials'] = 'true'
        return json.dumps(res, ensure_ascii=False)

if __name__ == '__main__':
    cherrypy.config.update({
        'environment': 'production',
        'log.screen': False,
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'show_tracebacks': False,
        'tools.encode.text_only': False,
    })
    cherrypy.quickstart(Server())
