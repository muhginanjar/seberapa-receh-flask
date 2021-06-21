from flask import Flask, request, render_template
import sqlite3 as sql
import collections
import json

app = Flask(__name__)
nama = ""

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/mulai',methods=['GET'])
def mulai():
    con = sql.connect('soal.db')
    cur = con.cursor()
    rows = cur.execute("select * from soal").fetchall()
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d["kategori"] = row[0]
        d["pertanyaan"] = row[1]
        objects_list.append(d)
    j = json.dumps(objects_list)
    with open("static/soal.json", "w") as f:
        f.write(j)
    con.close()
    nama = request.args.get('nama')
    return render_template("mulai.html",nama = nama)

@app.route('/selesai',methods=['POST'])
def selesai():
    nilai = 0
    datas = {}
    no = 0
    data = request.form.get('datas').split('||')
    pertanyaan = {}
    jawaban = {}
    kumpulan = ""
    for item in data:
        items = item.split(':')
        datas[no] = items
        pertanyaan[no] = items[0]
        jawaban[no] = items[1]
        no = no + 1
    
    con = sql.connect('soal.db') 
    cur = con.cursor() 
    rows = cur.execute("select * from soal WHERE pertanyaan in (?,?,?,?,?)",(pertanyaan[0],pertanyaan[1],pertanyaan[2],pertanyaan[3],pertanyaan[4])).fetchall() 
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d["kategori"] = row[0]
        d["pertanyaan"] = row[1]
        d["jawaban"] = row[2]
        d["keterangan"] = row[3]
        kumpulan = kumpulan + row[0] + "^" + row[1] + "^" + row[2] + "^" + row[3] + "||"
        objects_list.append(d)

    no = 0
    for rows in objects_list:
        if rows['jawaban'] == jawaban[no] : 
            nilai = nilai + 1
        no = no+1
    kumpulan = kumpulan + str(nilai)
    print(pertanyaan)
    return kumpulan

if __name__ == '__main__' :
    app.run(debug=True)