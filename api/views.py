from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import psycopg2
from json import loads as js_loads
from requests import get as req_get

conn = psycopg2.connect("dbname=test_task user=john")
cur = conn.cursor()

def get_list_slaves(request):
    obj_slaves = {}
    obj_slaves['slaves'] = []
    cur.execute("select name, surname from table_one;")
    result = cur.fetchall()
    for name,surname in result:
        obj_slaves['slaves'].append({'name':name, 'surname':surname})
    print(obj_slaves)
    return JsonResponse(obj_slaves)

def get_list_position(request):
    obj_position = {}
    obj_position['position'] = []
    cur.execute("select position from table_two;")
    result = cur.fetchall()
    for a in result:
        for b in a:
            obj_position['position'].append(b)
    return JsonResponse(obj_position)

def get_list_department(request):
    obj_department = {}
    obj_department['department'] = []
    cur.execute("select department from table_three;")
    result = cur.fetchall()
    for a in result:
        for b in a:
            obj_department['department'].append(b)
    return JsonResponse(obj_department)

def get_name_by_id(request, id):
    cur.execute(f'select name, table_one.surname, department, position from table_one,table_three where id_user={id} and table_one.surname=table_three.surname;')
    result = cur.fetchall()
    
    return HttpResponse(result)

def get_info_of_slaves(request):
    all_user = {}
    all_user['all_user'] = []
    cur.execute('select id_user, name, table_one.surname, department, position from table_one,table_three where table_one.surname=table_three.surname;')
    result = cur.fetchall()
    for id_user, name, surname, department, position in result:
        all_user['all_user'].append({"id": id_user, "name": name, "surname": surname, "department": department, "position": position})
    return JsonResponse(all_user)

def post_test(request):
    decode = request.body.decode('utf-8')
    js_req = js_loads(decode)
    req_obj_dept = req_get('http://localhost:8000/list_department')
    req_obj_pos = req_get('http://localhost:8000/list_position')
    if not js_req['position'] in req_obj_pos.json()['position'] and not js_req['department'] in req_obj_dept.json()['department']:
        return HttpResponse('position or department position or department is not existing! \nUse: \ndepartment: ' + str(req_obj_dept.json()['department']) + '\nposition: '+str(req_obj_pos.json()['position'])+'\n')
    cur.execute(f"INSERT INTO table_one (name,surname) VALUES ('{js_req['name']}', '{js_req['surname']}');")
    conn.commit()
    cur.execute(f"select max(id_user) from table_one;")
    cur.execute(f"insert into table_two (position) values('{js_req['position']}');")
    conn.commit()
    cur.execute(f"insert into table_three (department, position, surname) values ('{js_req['department']}', '{js_req['position']}', '{js_req['surname']}')")
    conn.commit()
    return HttpResponse('User created successfully!\n')
# Create your views here.
