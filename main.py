from __future__ import unicode_literals
import vk
import time
import xlwt
from flask import Flask
from flask import request
from flask import send_file

APP_ID = 6087533

def get_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)




app = Flask(__name__)

@app.route('/')
def index(words="",stop_words=""):
    words = str(request.args.get('words', words))
    stop_words = str(request.args.get('stop_words', stop_words))
    all = find(words, stop_words)
    #return str(all)
    return send_file('C://Users/Уля/PycharmProjects/base/base.xls')

def find(words_, stop_words_):
    access_token = ""
    api = get_api(access_token)
    wb = xlwt.Workbook()
    all = set()
    stop_words = stop_words_.split(",")
    words = words_.split(",")

    for word in words:
        off = 0
        my_groups = api.groups.search(q=word, offset=off)
        all_groups = []
        for i in range(3):

            my_groups = api.groups.search(q=word, offset=off, fields='members_count')
            first = 0

            for gr in my_groups:
                if first != 0:
                    if gr['members_count'] >= 1000:
                        one_gr = []
                        one_gr.append(gr['name'])
                        one_gr.append("https://vk.com/" + str(gr['screen_name']))
                        all.add(one_gr[1])
                        all_groups.append(one_gr)
                first += 1
            off += 21
            print(all_groups)
            time.sleep(1)

        ws = wb.add_sheet(word, cell_overwrite_ok=True)
        i = 0
        for gr in all_groups:
            ws.write(i, 0, xlwt.Formula('hyperlink("{}";"{}")'.format(gr[1], gr[0])))
            i += 1

    ws = wb.add_sheet("ALL", cell_overwrite_ok=True)
    i = 0
    for gr in all:
        ws.write(i, 0, gr)
        i += 1
    wb.save('base.xls')
    return(all)

if __name__ == "__main__":
    app.run(debug=True)
