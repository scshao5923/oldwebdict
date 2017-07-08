from bottle import route, run, static_file, request, template
import datetime
import socket
import sqlite3
import sys
from gtts import gTTS
#設定資料路徑
MY_PC='scshao5923-PC'
DB='dict.db'
if sys.platform[:3] == 'win':
    if socket.gethostname()==MY_PC:
        DATA_PATH='C:\\Users\\scshao5923\\SkyDrive\\BBC\\'
    else:
        DATA_PATH='C:\\DICT\\'    
else:
    DATA_PATH='./'
#得到本地ip    
localIP = socket.gethostbyname(socket.gethostname())

@route('/')
def indexPg():
    return template('index.html', {'ip':localIP,})

@route('/add')
def addPg():
    return template('add.html', {'ip':localIP,})

@route('/runAdd',method='POST')
def addRec():
##    name = request.forms.getunicode('name')
##    ty = request.forms.getunicode('ty')
##    pron = request.forms.getunicode('pron')
##    ch = request.forms.getunicode('ch')
##    sc1 = request.forms.getunicode('sc1')
##    ex1 = request.forms.getunicode('ex1')
##    sc2 = request.forms.getunicode('sc2')
##    ex2 = request.forms.getunicode('ex2')
##    sc3 = request.forms.getunicode('sc3')
##    ex3 = request.forms.getunicode('ex3')
    name = request.POST.name
    ty = request.POST.ty
    pron = request.POST.pron
    ch = request.POST.ch
    sc1 = request.POST.sc1
    ex1 = request.POST.ex1
    sc2 = request.POST.sc2
    ex2 = request.POST.ex2
    sc3 = request.POST.sc3
    ex3 = request.POST.ex3
    
    conn = sqlite3.connect(DATA_PATH+DB)
    cursor = conn.cursor()
    cursor.execute('select " " dummy from newword where name=?',(name,))
    values = cursor.fetchone()
    if not values:
        tdy=datetime.date.today()
        wkDat="{0:04}{1:02}{2:02}".format(tdy.year,tdy.month,tdy.day)
        cursor.execute('select max(id) dummy from newword where id like ?',(wkDat+'%',))
        ID=cursor.fetchone()[0]
        cursor.execute(
            'insert into newword (id, name, ty, pron, ch, sc1, ex1, sc2, ex2, sc3, ex3) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            ,(str(int(ID)+1) if ID else str(int(wkDat)*100), name, ty, pron, ch, sc1, ex1, sc2, ex2, sc3, ex3)
        )
    cursor.close()
    conn.commit()
    conn.close()
    return template('''
        <p>{{msg}}</p>
        <input type="button" value="繼續" onclick="javascript:location.href='http://{{ip}}/webdict/add'">
        '''
        ,{'msg':'新增完成!' if not values else name+':資料已存在!!!','ip':localIP,} 
    )

@route('/qry',method='GET')
def qryRec():
    if request.GET.qry:
        conn = sqlite3.connect(DATA_PATH+DB)
        c = conn.cursor()
        name=request.GET.name
        print('request.name:'+str(name))
        c.execute("SELECT * FROM newword where name like ? ORDER BY lower(name)",(name+'%',))
        result = c.fetchall()
        return template('make_table.html', {'rows':result,'ip':localIP,})
    else:
        return template('query.html')

@route('/edit/<name>', method='GET')
def edit_item(name):

    if request.GET.save:
##        ty = request.forms.getunicode('ty')
##        pron = request.forms.getunicode('pron')
##        ch = request.forms.getunicode('ch')
##        sc1 = request.forms.getunicode('sc1')
##        ex1 = request.forms.getunicode('ex1')
##        sc2 = request.forms.getunicode('sc2')
##        ex2 = request.forms.getunicode('ex2')
##        sc3 = request.forms.getunicode('sc3')
##        ex3 = request.forms.getunicode('ex3')
        ty = request.GET.ty
        pron = request.GET.pron
        ch = request.GET.ch
        sc1 = request.GET.sc1
        ex1 = request.GET.ex1
        sc2 = request.GET.sc2
        ex2 = request.GET.ex2
        sc3 = request.GET.sc3
        ex3 = request.GET.ex3
        print((ty, pron, ch, sc1, ex1, sc2, ex2, sc3, ex3, name))
        conn = sqlite3.connect(DATA_PATH+DB)
        c = conn.cursor()
        c.execute("UPDATE newword SET ty=?, pron=?, ch=?, sc1=?, ex1=?, sc2=?, ex2=?, sc3=?, ex3=? WHERE name=?", (ty, pron, ch, sc1, ex1, sc2, ex2, sc3, ex3, name))
        c.close()
        conn.commit()
        conn.close()
        return template('''
            <p>{{msg}}</p>
            <input type="button" value="繼續" onclick="javascript:location.href='http://{{ip}}/webdict'">
            '''
            ,{'msg':'更正完成!' if True else '', 'ip':localIP,} 
        )
    else:
        conn = sqlite3.connect(DATA_PATH+DB)
        c = conn.cursor()
        c.execute("SELECT * FROM newword WHERE name=?", (name,))
        row = c.fetchone()

        return template('edit.html', {'old':row, 'name':name, 'ip':localIP,})

@route('/del/<name>', method='GET')
def del_item(name):

    if request.GET.save:
        conn = sqlite3.connect(DATA_PATH+DB)
        c = conn.cursor()
        c.execute("DELETE FROM newword WHERE name=?", (name, ))
        c.close()
        conn.commit()
        conn.close()
        return template('''
            <p>{{msg}}</p>
            <input type="button" value="繼續" onclick="javascript:location.href='http://{{ip}}/webdict'">
            '''
            ,{'msg':'刪除完成!' if True else '', 'ip':localIP, } 
        )
    else:
        conn = sqlite3.connect(DATA_PATH+DB)
        c = conn.cursor()
        c.execute("SELECT * FROM newword WHERE name=?", (name,))
        row = c.fetchone()

        return template('del.html', {'old':row, 'name':name, 'ip':localIP, })

@route('/pronounce/<name>', method='GET')
def pronounce_item(name):
    tts=gTTS(text=name,lang='en')
    print('pronounce:'+name)
    tts.save('c:/apache24/htdocs/temp/'+name+'.mp3')
    return template("<audio src='http://{{ip}}/temp/{{file}}' autoplay>",{'file':name+'.mp3', 'ip':localIP,})

@route('/test')
def myTest():
    return template('test.html',{'name':'邵世昌'})
	
if __name__ == "__main__":
	run(host=localIP, path='/webdict', port=80, debug=True)
