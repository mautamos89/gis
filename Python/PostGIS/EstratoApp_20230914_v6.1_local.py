import tkinter
from tkinter import StringVar,Scrollbar,LEFT,CENTER
from tkinter import ttk,messagebox
from time import strftime

# Mensaje de bienvenida

messagebox.showinfo('Le damos la bienvenida!', """
La aplicación "Estrato BaseMaestra" ha sido diseñada por
el DAP para facilitar la consulta interna de la información
alfanumérica y geográfica perteneciente a la Base Oficial
de Estratificación Socioeconómica del Distrito de Cali.\n
Si tiene alguna pregunta o desea verificar una imprecisión,
se sugiere utilizar otras plataformas de la Alcaldía de Cali,
como SAUL, Geovisor IDESC y Geoportal Catastral.
""")

# Créditos y desarrollo

print("inicio de programa: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
print('título: aplicación de escritorio para consultar la Base Oficial de Estratificación Socioeconómica del Distrito de Cali publicada en IDESC.'.upper())
print('licencia: Creative Commons. Condiciones de: atribución, no comercial, no derivada y compartir igual.'.upper())
print('requerimientos: sistema operativo windows, memoria ram 2gb, conexión a intranet e internet alcaldía.'.upper())
print('grupo de desarrollo: estratificación socioeconómica, departamento administrativo de planeación - cali, 2023 ©.'.upper())
print('autor: mauricio tabares mosquera.'.upper())
print('profesión: geógrafo, especialista sig.'.upper())
print('versión: 6.1 | fecha: 2023-09-16.'.upper())

# GUI: Ventana principal

window = tkinter.Tk()
style=ttk.Style()
window.title('Base Maestra de Estratificación | Estratificación Socioeconómica - Cali, 2023 ©')

# Variables de búsqueda

usr_idpredio=StringVar()
usr_npn=StringVar()
usr_mlad=StringVar()

# Recuadro abajo

frame=tkinter.Frame(window)
frame.grid(column=0,row=1)

# Recuadro arriba

frameLeft=tkinter.Frame(window)
frameLeft.grid(column=0,row=0,sticky='nw')

# Recuadro # 1: información del Predio

fra_usr_idpredio = tkinter.LabelFrame(frameLeft,text='Información del predio',font="TkDefaultFont 10")
fra_usr_idpredio.grid(row=0,column=0,sticky='n',padx=20,pady=10)

# Recuadro # 1: etiquetas

lab_cfg1,lab_cfg2,lab_cfg3 = "TkDefaultFont 10","#F5DEB3","#354A54"
#lab_usr_idpredio = tkinter.Label(fra_usr_idpredio,text='ID Predio:',font=lab_cfg1,fg=lab_cfg2,bg=lab_cfg3)
lab_usr_idpredio = tkinter.Label(fra_usr_idpredio,text='ID Predio:',font=lab_cfg1)
lab_usr_idpredio.grid(row=0,column=0,sticky='nw')
lab_npn = tkinter.Label(fra_usr_idpredio,text='NPN:',font=lab_cfg1)
lab_npn.grid(row=1,column=0,sticky='nw')
lab_mlad = tkinter.Label(fra_usr_idpredio,text='Manzana-Lado:',font=lab_cfg1)
lab_mlad.grid(row=2,column=0,sticky='nw')

# Recuadro # 1: entrada de búsqueda

ent_usr_idpredio = tkinter.Entry(fra_usr_idpredio,width=10,textvariable=usr_idpredio)
ent_usr_idpredio.grid(row=0,column=1,sticky='news')
ent_usr_npn = tkinter.Entry(fra_usr_idpredio,width=31,textvariable=usr_npn)
ent_usr_npn.grid(row=1,column=1,sticky='news')
ent_usr_mlad = tkinter.Entry(fra_usr_idpredio,width=10,textvariable=usr_mlad)
ent_usr_mlad.grid(row=2,column=1,sticky='news')

# Recuadro # 1: configuración de estilo de widgets

for widget in fra_usr_idpredio.winfo_children(): widget.grid_configure(padx=5,pady=12)

# Recuadro # 3: cuadro de resultados

fra_resul = tkinter.LabelFrame(frame,text='Resultados',font="TkDefaultFont 10")
fra_resul.grid(row=0,column=1,sticky='n',padx=10,pady=8)

# Barra vertical: insertar

scr_bar = Scrollbar(fra_resul)
scr_bar.grid(row=2,column=1,sticky='ns')

# Recuadro # 3: vista de árbol con barra vertical

tview = ttk.Treeview(fra_resul, yscrollcommand=scr_bar.set, selectmode="extended",columns=('c_0','c_1','c_2','c_3','c_4','c_5','c_6','c_7','c_8'), show='headings',height=20)
style.configure('Treeview.Heading',font=('TkDefaultFont',8,'bold'))

# Barra vertical: configurar

scr_bar.config(command=tview.yview)

# Columnas

tview.column('c_0', anchor=CENTER,minwidth=0, width=50)
tview.column('c_1', anchor=CENTER,minwidth=0, width=80)
tview.column('c_2', anchor=CENTER,minwidth=0, width=200)
tview.column('c_3', minwidth=0, width=310)
tview.column('c_4', minwidth=0, width=100)
tview.column('c_5', anchor=CENTER,minwidth=0, width=60)
tview.column('c_6', minwidth=0, width=160)
tview.column('c_7', minwidth=0, width=60)
tview.column('c_8', anchor=CENTER,minwidth=0, width=70)

# Etiquetas

tview.heading('c_0', text='#',command=lambda: sort(tview,'c_0'))
tview.heading('c_1', text='ID Predio',command=lambda: sort(tview,'c_1'))
tview.heading('c_2', text='NPN',command=lambda: sort(tview,'c_2'))
tview.heading('c_3', text='Dirección',command=lambda: sort(tview,'c_3'))
tview.heading('c_4', text='Manzana-Lado',command=lambda: sort(tview,'c_4'))
tview.heading('c_5', text='Estrato',command=lambda: sort(tview,'c_5'))
tview.heading('c_6', text='Tipo Estrato',command=lambda: sort(tview,'c_6'))
tview.heading('c_7', text='Atípica',command=lambda: sort(tview,'c_7'))
tview.heading('c_8', text='Estrato [A]',command=lambda: sort(tview,'c_8'))

# Color para registros

tview.tag_configure('par', background="white")
tview.tag_configure('impar', background="#CEE6F3")
tview.grid(row=2,column=0, padx=10,pady=10)
print('Interfaz gráfica generada con éxito'.upper())

# Funcion: comparar diccionarios y actualizar a partir de llaves comunes

def compare_and_delete(dict_a, dict_b):
                common_keys = set(dict_a.keys()) & set(dict_b.keys()) # Obtener las llaves comunes en diccionarios
                dict_a_common = {key: dict_a[key] for key in common_keys} # Crear diccionario temporal con llaves y valores comunes
                dict_a.clear() # Borrar contenido de diccionario
                dict_a.update(dict_a_common) # Actualizar el diccionario con llaves y valores comunes

# Función: Conectar a servidor y base de datos PostgreSQL

def con_sql():
    global con,nreg,ver,bdm
    print("Conexión SQL inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    import psycopg2,datetime
    try:
        # Local
        con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port= '5432'
        )
    except:
        print('Base de datos PostgreSQL Planeación: sin conexión'.upper())
    else:
        print('Base de datos PostgreSQL Planeación: conexión exitosa'.upper())
        try:
            bdm='dat_pdt_est_estrato_urbano_expansion' # Base maestra de estratificación
            col_list ="""count(*)""" # Columnas para consulta SQL
            query = fr""" 
            select {col_list}
            from {bdm}
            ;""" #Query SQL
            cursor_obj=con.cursor()
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj.execute(query)
            for row in cursor_obj: nreg=row[0] # Row es igual al index de columnas en SQL Query
            ver=(datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m-%d") # FECHA DE CORTE A PARTIR DE FECHA
        except:
            print('Consulta SQL incorrecta'.upper())
        else:
            print(f'Consulta SQL exitosa'.upper())
con_sql()

def con_sql2():
    global con2
    print("Conexión SQL inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    import psycopg2
    try:
        # Local
        con2 = psycopg2.connect(
        database="postgis_default",
        user="postgres",
        password="postgres",
        host="localhost",
        port= '5432'
        )
    except:
        print('Base de datos PostgreSQL Catastro: sin conexión'.upper())
    else:
        print(f'Base de datos PostgreSQL Catastro: conexión exitosa'.upper())

# Función: Consultar la base de datos en el servidor PostgreSQL

def sql_query():
    try:
        con_sql()
        con_sql2()
        global d
        sql_idpre=usr_idpredio.get().strip() # Variables
        sql_npn=usr_npn.get().strip() # Variables
        sql_mzn=usr_mlad.get().strip() # Variables
        d,d_geo={},{}
        bd_atip='dat_pdt_est_estrato_atipicos' # Tabla de atípicos
        bd_cat='dat_cat_bas_catastral' # Tabla catastral
        col_list1 ="""ide.estidpredi,ide.estsesemal,ide.estestrato,ide.esttipestr,ati.eatestado,ati.eatestrato""" # Columnas consulta SQL DAP
        col_list3="""ide.id_predio,ide.npn,ide.direccion""" # Columnas consulta SQL Catastro (Manzana-Lado)
        
        if usr_idpredio.get():
            # Diccionario 1
            query = fr"""
            select {col_list1}
            from {bdm} as ide
            left join {bd_atip} as ati
            on ide.estidpredi=ati.eatidpredi
            where ide.estidpredi={sql_idpre}
            order by ide.estidpredi
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con.cursor()
            cursor_obj.execute(query)
            for row in cursor_obj: # Row index refiere la posición de columnas en SQL Query
                id_predio=row[0]
                sesemanlad=row[1]
                est_def=row[2]
                tipo_est=row[3]
                est_atipes=row[4]
                est_atiestra=row[5]
                d[id_predio]=[sesemanlad,est_def,tipo_est,est_atipes,est_atiestra] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con.close()
            #print(f'd_query1: {list(d.items())[:5]}') # Imprimir los primeros cinco elementos del diccionario
            
            #Diccionario 2
            query = fr"""
            select {col_list3}
            from {bd_cat} as ide
            where ide.id_predio={sql_idpre}
            order by ide.id_predio
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con2.cursor()
            cursor_obj.execute(query)
            if cursor_obj.rowcount == 0: d_geo[None]=[None,None] # Regresar nulos si la consulta es vacía
            for row in cursor_obj: # Row index refiere la posición de columnas en SQL Query
                id_predio=row[0]
                npn=row[1]
                direccion=row[2]
                d_geo[id_predio]=[npn,direccion] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con2.close()
            for key,value in d_geo.items(): d[key].extend(value) if key in d else None # Unir diccionarios con resultados por llave
        
        elif usr_npn.get(): # Buscar por NPN invierte el orden de los diccionarios
            # Diccionario 2
            query = fr"""
            select {col_list3}
            from {bd_cat} as ide
            where ide.npn like '%{sql_npn}%'
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con2.cursor()
            cursor_obj.execute(query)
            if cursor_obj.rowcount == 0: d_geo[None]=[None,None]
            for row in cursor_obj: # Row es igual al index de columnas en SQL Query
                id_predio=row[0]
                npn=row[1]
                direccion=row[2]
                d_geo[id_predio]=[npn,direccion] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con2.close()

            # Diccionario 1
            idpredio_values = ','.join(str(key) for key in d_geo.keys()) # Unir valores para consulta SQL
            query = fr"""
            select {col_list1}
            from {bdm} as ide
            left join {bd_atip} as ati
            on ide.estidpredi=ati.eatidpredi
            where ide.estidpredi in ({idpredio_values})
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con.cursor()
            cursor_obj.execute(query)
            rows = cursor_obj.fetchall() # Procesar la consulta y obtener los resultados
            for row in rows: # Procesar las filas y guardar a diccionario
                id_predio=int(row[0])
                sesemanlad=row[1]
                est_def=row[2]
                tipo_est=row[3]
                est_atipes=row[4]
                est_atiestra=row[5]
                d[id_predio]=[sesemanlad,est_def,tipo_est,est_atipes,est_atiestra]
            cursor_obj.close()
            con.close()
            #print(f'd_query1: {list(d.items())[:5]}') # Imprimir los primeros cinco elementos del diccionario
            for key,value in d_geo.items(): d[key].extend(value) if key in d else None # Unir diccionarios con resultados por llave
            compare_and_delete(d,d_geo)
            d={k: v for k, v in sorted(d.items())} # Ordenar el diccionario por la llave  
        
        elif usr_mlad.get():
            # Diccionario 1
            query = fr"""
            select {col_list1}
            from {bdm} as ide
            left join {bd_atip} as ati
            on ide.estidpredi=ati.eatidpredi
            where ide.estsesemal like '%{(sql_mzn).upper()}%'
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con.cursor()
            cursor_obj.execute(query)
            for row in cursor_obj: # Row es igual al index de columnas en SQL Query
                id_predio=row[0]
                sesemanlad=row[1]
                est_def=row[2]
                tipo_est=row[3]
                est_atipes=row[4]
                est_atiestra=row[5]
                d[id_predio]=[sesemanlad,est_def,tipo_est,est_atipes,est_atiestra] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con.close()
            #print(f'd_query1: {list(d.items())[:5]}') # Imprimir los primeros cinco elementos del diccionario
            
            # Diccionario 2
            idpredio_values = ','.join(str(key) for key in d.keys()) # Unir valores para consulta SQL
            query2 = fr"""
                select {col_list3}
                from {bd_cat} as ide
                where ide.id_predio in ({idpredio_values})
                ;
            """ # Consulta SQL
            #print(query2)
            cursorobj = con2.cursor()
            cursorobj.execute(query2)
            rows = cursorobj.fetchall() # Procesar la consulta y obtener los resultados
            for row in rows: # Procesar las filas y guardar a diccionario
                id_predio=row[0]
                npn=row[1]
                direccion=row[2]
                d_geo[id_predio]=[npn, direccion]
            cursorobj.close()
            con2.close()
            for key,value in d_geo.items(): d[key].extend(value) if key in d else None # Unir diccionarios con resultados por llave
            compare_and_delete(d,d_geo)
            d={k: v for k, v in sorted(d.items())} # Ordenar el diccionario por la llave        
    except:
        print('Consulta SQL incorrecta'.upper())
    else:
        print(f'Consulta SQL exitosa. Registros cargados: {len(d)}'.upper())
    #print(f'd_geo: {list(d_geo.items())[:5]}') # Imprimir los primeros cinco elementos del diccionario
    #print(f'd_query2: {list(d.items())[:5]}') # Imprimir los primeros cinco elementos del diccionario
    print("Conexión SQL terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

def sql_query_map():
    try:
        con_sql()
        con_sql2()
        global d
        sql_idpre=usr_idpredio.get().strip() # Variables
        sql_npn=usr_npn.get().strip() # Variables
        d,d_geo={},{}
        bd_coords='cat_bas_terrenos' # Tabla de coordenadas en grados decimales por terreno
        bd_atip='dat_pdt_est_estrato_atipicos'
        bd_cat='dat_cat_bas_catastral'
        col_list1 ="""ide.estidpredi,ide.estsesemal,ide.estestrato,ide.esttipestr,ati.eatestado,ati.eatestrato""" # Columnas para consulta SQL
        col_list2="""ide.id_predio,ide.npn,ide.direccion,round(st_y(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lat_y,
            round(st_x(st_transform(st_pointonsurface(geom),4326))::numeric,5) as lon_x""" # PARA IDPREDIO Y NPN
        
        if usr_idpredio.get():
            # Diccionario 1
            query = fr"""
            select {col_list1}
            from {bdm} as ide
            left join {bd_atip} as ati
            on ide.estidpredi=ati.eatidpredi
            where ide.estidpredi={sql_idpre}
            order by ide.estidpredi
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con.cursor()
            cursor_obj.execute(query)
            for row in cursor_obj: # Row es igual al index de columnas en SQL Query
                id_predio=row[0]
                sesemanlad=row[1]
                est_def=row[2]
                tipo_est=row[3]
                est_atipes=row[4]
                est_atiestra=row[5]
                d[id_predio]=[sesemanlad,est_def,tipo_est,est_atipes,est_atiestra] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con.close()
            #print(f'd_query1: {list(d.items())[:5]}') # Imprimir elementos
            
            # Diccionario 2
            query = fr"""
            select {col_list2}
            from {bd_coords} as pnt
            right join {bd_cat} as ide
            on ide.idterreno=pnt.conexion
            where ide.id_predio={sql_idpre}
            order by ide.id_predio
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con2.cursor()
            cursor_obj.execute(query)
            for row in cursor_obj: # Row es igual al index de columnas en SQL Query
                id_predio=row[0]
                npn=row[1]
                direccion=row[2]
                lat_y=row[3]
                lon_x=row[4]
                d_geo[id_predio]=[npn,direccion,lat_y,lon_x] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con2.close()
            for key,value in d_geo.items(): d[key].extend(value) if key in d else None # Unir diccionarios con resultados por llave
        
        elif usr_npn.get(): # Buscar por NPN invierte el orden de los diccionarios
            # Diccionario 2
            query = fr"""
            select {col_list2}
            from {bd_coords} as pnt
            right join {bd_cat} as ide
            on ide.idterreno=pnt.conexion
            where ide.npn = '{sql_npn}'
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con2.cursor()
            cursor_obj.execute(query)
            if cursor_obj.rowcount == 0: d_geo[None]=[None,None,None,None]
            for row in cursor_obj: # Row es igual al index de columnas en SQL Query
                id_predio=row[0]
                npn=row[1]
                direccion=row[2]
                lat_y=row[3]
                lon_x=row[4]
                d_geo[id_predio]=[npn,direccion,lat_y,lon_x] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con2.close()
            
            # Diccionario 1
            idpredio_values = ','.join(str(key) for key in d_geo.keys()) # Unir valores para consulta SQL
            query = fr"""
            select {col_list1}
            from {bdm} as ide
            left join {bd_atip} as ati
            on ide.estidpredi=ati.eatidpredi
            where ide.estidpredi in ({idpredio_values})
            ;""" # Consulta SQL
            print(f'Ejecutando consulta SQL: \n{query}\n')
            cursor_obj=con.cursor()
            cursor_obj.execute(query)
            rows = cursor_obj.fetchall() # Procesar la consulta y obtener los resultados
            for row in rows: # Procesar las filas y guardar a diccionario
                id_predio=row[0]
                sesemanlad=row[1]
                est_def=row[2]
                tipo_est=row[3]
                est_atipes=row[4]
                est_atiestra=row[5]
                d[id_predio]=[sesemanlad,est_def,tipo_est,est_atipes,est_atiestra]
            cursor_obj.close()
            con.close()
            #print(f'd_query1: {list(d.items())[:5]}') # Imprimir elementos del diccionario
            for key,value in d_geo.items(): d[key].extend(value) if key in d else None # Unir diccionarios con resultados por llave
    except:
        print('Consulta SQL incorrecta'.upper())
    else:
        print(f'Consulta SQL exitosa. Registros cargados: {len(d)}'.upper())
    #print(f'd_geo: {list(d_geo.items())[:5]}') # Imprimir los primeros cinco elementos del diccionario
    #print(f'd_query2: {list(d.items())[:5]}') # Imprimir los primeros cinco elementos del diccionario
    print("Conexión SQL terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Función: ordenar columnas por valores

def sort(tview,col):
    itemlist=list(tview.get_children(''))
    itemlist.sort(key=lambda x: tview.set(x,col))
    for index,iid in enumerate(itemlist):
        tview.move(iid,tview.parent(iid),index)

# Función: reeemplazar resultados: Tipo estrato

d1 = {
    '1':'Urbano',
    '6':'Rural',
    '8':'Residencial no estratificado',
    '9':'No residencial',
    None:'Sin estrato',
}
def x(a):
    if a in d1.keys():
      return d1[a]
    else:
      return a

# Función: reeemplazar resultados - Manzana-Lado

d2 = {
    None:'Sin lado'
}
def y(a):
    if a in d2.keys():
      return d2[a].upper()
    else:
      return a.upper()

# Función reeemplazar resultados - Dirección

d3 = {
    None:'Sin dirección'
}
def z(a):
    if a in d3.keys():
      return d3[a].upper()
    else:
      return a.upper()

# Función: reeemplazar resultados - Atípica

d4 = {
    'A':'Activa',
    'I':'Inactiva',
    None:'No'
}
def w(a):
    if a in d4.keys():
      return d4[a]
    else:
      return a

# Función: leyenda, predios y colores, reeemplazar resultados - Estratos

d5 = {# Diccionario con datos de valor: etiqueta, color y separación
    '1':['Estrato 1','#FF8566',0],
    '2':['Estrato 2','#F7F366',0],
    '3':['Estrato 3','#6FB88E',0.1],
    '4':['Estrato 4','#FFC165',0],
    '5':['Estrato 5','#6584FF',0],
    '6':['Estrato 6','#C184FF',0],
    '8':['Sin estratificar','#CCCCCC',0],
    '9':['No residencial','#FFFFFF',0]
}
def v(a):
    if a in d5.keys():
        return d5[a][0]
    else:
        return a

# Función: buscar predio

def bus_predio():
    print("Búsqueda inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    try:
        # Funcion conexion
        sql_query()
        num,cnt=1,[]
        tview.delete(*tview.get_children()) # Limpiar el árbol de resultados
        idPre=usr_idpredio.get().strip() # Variables
        npn=usr_npn.get().strip() # Variables
        mLad=usr_mlad.get().strip().upper() # Variables
        if usr_idpredio.get():
            for id in d:
                np,dir,mla,est,tes,ati,ati_estra=d[id][5],d[id][6],d[id][0],d[id][1],d[id][2],d[id][3],d[id][4]
                if id == int(idPre):
                    if num % 2 == 0:
                        tview.insert('', 'end', values=(int(num),id,np,z(dir),y(mla),est,x(tes),w(ati),w(ati_estra)),tags=('par',))
                    else:
                        tview.insert('', 'end', values=(int(num),id,np,z(dir),y(mla),est,x(tes),w(ati),w(ati_estra)),tags=('impar',))
                    num+=1
                    cnt.append(idPre)
            while True:
                if len(cnt) == 0:
                    messagebox.showwarning('Predio no encontrado!', 'ID Predio: {a} - Resultados: {b}\n \n¿Predio activo o retirado?\nRevisa SIGCAT'.format(a=idPre,b=len(cnt)))
                    break
                else:
                    print('Predio encontrado!', f'ID Predio: {idPre} - Resultados: {len(cnt)}')
                    messagebox.showinfo('Predio encontrado!', 'ID Predio: {a}\nResultados: {b}'.format(a=idPre,b=len(cnt)))
                    break
        elif usr_npn.get():
            for id in d:
                np,dir,mla,est,tes,ati,ati_estra=d[id][5],d[id][6],d[id][0],d[id][1],d[id][2],d[id][3],d[id][4]
                if npn in np:
                    if num % 2 == 0:
                        tview.insert('', 'end', values=(int(num),id,np,z(dir),y(mla),est,x(tes),w(ati),w(ati_estra)),tags=('par',))
                    else:
                        tview.insert('', 'end', values=(int(num),id,np,z(dir),y(mla),est,x(tes),w(ati),w(ati_estra)),tags=('impar',))
                    num+=1
                    cnt.append(npn)
            while True:
                if len(cnt) == 0:
                    messagebox.showwarning('Predio no encontrado!', 'NPN: {a} - Resultados: {b}\n \n¿Predio activo o retirado?\nRevisa SIGCAT'.format(a=npn,b=len(cnt)))
                    break
                else:
                    print('Predio encontrado!', f'NPN: {npn} - Resultados: {len(cnt)}')
                    messagebox.showinfo('Predio encontrado!', 'NPN: {a}\nResultados: {b}'.format(a=npn,b=len(cnt)))
                    break
        elif usr_mlad.get():
            for id in d:
                np,dir,mla,est,tes,ati,ati_estra=d[id][5],d[id][6],d[id][0],d[id][1],d[id][2],d[id][3],d[id][4]
                if mLad in y(mla):
                    if num % 2 == 0:
                        tview.insert('', 'end', values=(int(num),id,np,z(dir),y(mla),est,x(tes),w(ati),w(ati_estra)),tags=('par',))
                    else:
                        tview.insert('', 'end', values=(int(num),id,np,z(dir),y(mla),est,x(tes),w(ati),w(ati_estra)),tags=('impar',))
                    num+=1
                    cnt.append(mla)
            while True:
                if len(cnt) == 0:
                    messagebox.showwarning('Manzana no encontrada!', 'Manzana-Lado: {a} - Resultados: {b}\n \n¿Lado de manzana existe?\nRevisa EsUrbano'.format(a=mLad,b=len(cnt)))
                    break
                else:
                    print('Manzana encontrada!', f'Manzana-Lado: {mLad} - Resultados: {len(cnt)}')
                    messagebox.showinfo('Manzana encontrada!', 'Manzana-Lado: {a}\nResultados: {b}'.format(a=mLad,b=len(cnt)))
                    break
        else:
            messagebox.showwarning('Sin resultados!', 'Ingresa un valor correcto!')
    except:
        messagebox.showwarning('Sin resultados!', 'No se pudo generar el listado!')
    print("Búsqueda terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Función: copiar registros seleccionados

def copy(event):
    print("Copia de registros inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    sel = tview.selection() # Identificar elementos seleccionados
    window.clipboard_clear()  # Limpiar el portapapeles
    headings = [tview.heading("#{}".format(i), "text") for i in range(len(tview.cget("columns")) + 1)] # Copiar los encabezados
    window.clipboard_append("\t".join(headings) + "\n")
    for item in sel:
        values = [tview.item(item, 'text')] # Recuperar los valores de la fila
        values.extend(tview.item(item, 'values'))
        window.clipboard_append("\t".join(values) + "\n") # Adjuntar y separar valores por tabulación y salto de línea al portapapeles
        print(values[1:])
    print("Copia de registros terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
tview.bind('<Control-c>', copy)

# Función: reloj en tiempo real --> FALTA INSERTAR EN LABEL DE ABAJO EN GRID

""" def reloj():
    currentime = time.strftime ("%H:%M:%S")
    lab_reloj.config (text=currentime)
    lab_reloj.after(1000, reloj) """

# Función: abrir mapa en ventana nueva

def ruta_predio():
    print("Generar ruta al predio inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    import webbrowser
    try:
        num,cnt=1,[]
        idPre=usr_idpredio.get().strip() # Variables
        npn=usr_npn.get().strip() # Variables
        sql_query_map()
        if usr_idpredio.get():
            for id in d:
                np,lat,lon=d[id][5],d[id][7],d[id][8]
                if id == int(idPre):
                    print(f'ID Predio: {idPre} - Latitud: {lat} - Longitud: {lon}'.upper())
                    num+=1
                    cnt+=(lat,lon)
            while True:
                    if len(cnt) == 0:
                        messagebox.showwarning('Ruta no generada!', 'ID Predio: {a} - Resultados: {b}\n \n¿Predio activo o retirado?\nRevisa SIGCAT'.format(a=idPre,b=len(cnt)))
                        break
                    elif type(float(cnt[0])) == float and type(float(cnt[1])) == float:
                        messagebox.showinfo('Consulta exitosa!', 'Ruta generada en Google Maps!')
                        url_ruta=f'https://www.google.com/maps/dir/?api=1&origin=3.45475,-76.53436&destination={cnt[0]},{cnt[1]}&travelmode=driving'
                        webbrowser.open(url_ruta)
                        break
                        # URL # 3 RUTA
                        #https://www.google.com/maps/dir/?api=1&origin=Paris%2CFrance&destination=Cherbourg%2CFrance&travelmode=driving&waypoints=Versailles%2CFrance%7CChartres%2CFrance%7CLe+Mans%2CFrance%7CCaen%2CFrance
                        #https://www.google.com/maps/dir/?api=1&origin=3.45475,-76.53436&destination=3.38862,-76.55756&travelmode=driving
                    else: # No sé si borrar esta línea
                        print('No se pudo obtener las coordenadas')
        elif usr_npn.get():
            for id in d:
                np,lat,lon=d[id][5],d[id][7],d[id][8]
                if np == npn.lower().strip():
                    print(f'NPN: {np} - Latitud: {lat} - Longitud: {lon}'.upper())
                    num+=1
                    cnt+=(lat,lon)
            while True:
                    if len(cnt) == 0:
                        messagebox.showwarning('Predio no encontrado!', 'NPN: {a} - Resultados: {b}\n \n¿Predio activo o retirado?\nRevisa SIGCAT'.format(a=npn,b=len(cnt)))
                        break
                    elif type(float(cnt[0])) == float and type(float(cnt[1])) == float:
                        messagebox.showinfo('Consulta exitosa!', 'Ruta generada en Google Maps!')
                        url_ruta=f'https://www.google.com/maps/dir/?api=1&origin=3.45475,-76.53436&destination={cnt[0]},{cnt[1]}&travelmode=driving'
                        webbrowser.open(url_ruta)
                        break
                    else: # No sé si borrar esta línea
                        print('No se pudo obtener las coordenadas')
        else:
            messagebox.showwarning('Sin resultados!', 'Ingresa un valor ID Predio o NPN!')
    except: 
        messagebox.showwarning('No se pudo generar la ruta!', 'Revisa las coordenadas!\nPredio sin conexión a terreno geográfico!')
    else:
        print("generar ruta al predio terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

def abrir_mapa():
    print("Localización predio inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    import webbrowser
    try:
        num,cnt=1,[]
        idPre=usr_idpredio.get().strip() # Variables
        npn=usr_npn.get().strip() # Variables
        sql_query_map()
        if usr_idpredio.get():
            for id in d:
                np,lat,lon=d[id][5],d[id][7],d[id][8]
                if id == int(idPre):
                    print(f'ID Predio: {idPre} - Latitud: {lat} - Longitud: {lon}'.upper())
                    num+=1
                    cnt+=(lat,lon)
            while True:
                    if len(cnt) == 0:
                        messagebox.showwarning('Predio no encontrado!', 'ID Predio: {a} - Resultados: {b}\n \n¿Predio activo o retirado?\nRevisa SIGCAT'.format(a=idPre,b=len(cnt)))
                        break
                    elif type(float(cnt[0])) == float and type(float(cnt[1])) == float:
                        messagebox.showinfo('Consulta exitosa!', 'Predio localizado en Google Maps!')
                        #url_mapa=f'https://www.google.com/maps/search/{cnt[0]},%20{cnt[1]}'
                        url_mapa=f'https://maps.google.com/?&t=h&q={cnt[0]},{cnt[1]}&ll={cnt[0]},{cnt[1]}&z=18'
                        webbrowser.open(url_mapa)
                        break

                        #URL # 1
                        #https://www.google.com/maps/search/3.38862,%20-76.55756 ABRIR ENLACE EN PÁGINA? MEJORA RENDIMIENTO?
                        
                        #URL # 2 WORKING
                        #http://maps.google.com/maps?&t=h&z=19&q=loc:3.38862+-76.55756 # WORKING, CENTERED, NO ZOOM
                        #z is the zoom level (1-20)
                        #t is the map type ("m" map, "k" satellite, "h" hybrid, "p" terrain, "e" GoogleEarth)
                        #q is the search query, if it is prefixed by loc: then google assumes it is a lat lon separated by a + as space
                        #https://maps.google.com/?q=3.38862,-76.55756&z=20
                        #https://maps.google.com/?&t=h&q=38.6531004,-90.243462&ll=38.6531004,-90.243462&z=19 # WORKING, NO CENTERED, ZOOM
                        #https://maps.google.com/?&t=h&q=3.38862,-76.55756&ll=3.38862,-76.55756&z=18
                    else: # No sé si borrar esta línea
                        print('No se pudo obtener las coordenadas')
        elif usr_npn.get():
            for id in d:
                np,lat,lon=d[id][5],d[id][7],d[id][8]
                if np == npn.lower().strip():
                    print(f'NPN: {np} - Latitud: {lat} - Longitud: {lon}'.upper())
                    num+=1
                    cnt+=(lat,lon)
            while True:
                    if len(cnt) == 0:
                        messagebox.showwarning('Predio no encontrado!', 'NPN: {a} - Resultados: {b}\n \n¿Predio activo o retirado?\nRevisa SIGCAT'.format(a=npn,b=len(cnt)))
                        break
                    elif type(float(cnt[0])) == float and type(float(cnt[1])) == float:
                        messagebox.showinfo('Consulta exitosa!', 'Predio localizado en Google Maps!')
                        url_mapa=f'https://maps.google.com/?&t=h&q={cnt[0]},{cnt[1]}&ll={cnt[0]},{cnt[1]}&z=18'
                        webbrowser.open(url_mapa)
                        break
                    else: # No sé si borrar esta línea
                        print('No se pudo obtener las coordenadas')
        else:
            messagebox.showwarning('Sin resultados!', 'Ingresa un valor ID Predio o NPN!')
    except: 
        messagebox.showwarning('No se pudo generar el mapa!', 'Revisa las coordenadas!\nPredio sin conexión a terreno geográfico!')
    else:
        print("Localización predio terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Función: limpiar consulta

def limp():
    print("Limpieza inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    tview.delete(*tview.get_children())
    ent_usr_idpredio.delete(0, 'end')
    ent_usr_npn.delete(0, 'end')
    ent_usr_mlad.delete(0, 'end')
    messagebox.showinfo('Proceso realizado!', 'Limpieza realizada con éxito!')
    print("Limpieza terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Función: certificar predio

def cert():
    print("Certificación inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
    import cv2,os
    from PIL import Image
    from tkinter.filedialog import askopenfilename
    try:
        num,cnt=1,[]
        idPre=usr_idpredio.get().strip() # Variables
        npn=usr_npn.get().strip() # Variables
        sql_query()
        if usr_idpredio.get():
            for id in d:
                np,est=d[id][5],d[id][1]
                if id == int(idPre) and est not in ('8','9'):
                    #print(f'{idPre}={id}|{np}={npn}')
                    num+=1
                    cnt.insert(0,id)
                    cnt.insert(1,np)
                    cnt.insert(2,est)
                    #print(cnt)
            while True:
                if len(cnt) == 0:
                    messagebox.showwarning('Certificado no generado!', 'ID Predio: {a} - Resultados: {b}\n \n¿Predio activo con estrato residencial?\nRevisa SIGCAT y Tipo Estrato'.format(a=idPre,b=len(cnt)))
                    break
                else:
                    try:
                        messagebox.showinfo('Generando certificado!','Selecciona la plantilla .JPG!')
                        cert_plantilla=askopenfilename(filetypes=[('Imágenes','*.jpg')])
                        #print(cert_plantilla)
                        template=cv2.imread(cert_plantilla)
                        cv2.putText(template,f'{cnt[1]}',(2181,2525), cv2.FONT_HERSHEY_SIMPLEX,3.75,(0,0,0),16,cv2.LINE_AA)
                        cv2.putText(template,cnt[2],(1865,3035), cv2.FONT_HERSHEY_SIMPLEX,3.75,(0,0,0),16,cv2.LINE_AA)
                        cv2.putText(template,f'{strftime("%Y-%m-%d %H:%M:%S")}',(3580,4000), cv2.FONT_HERSHEY_SIMPLEX,3.75,(0,0,0),10,cv2.LINE_AA)
                        img_cert=os.path.join(os.path.dirname(cert_plantilla),fr'Certificado_{cnt[0]}.jpg')
                        #img_cert=rf'd:\Certificado_{cnt[0]}.jpg'
                        cv2.imwrite(img_cert,template)
                        #print('Certificado en jpg')
                        image_obj = Image.open(img_cert).convert('RGB')
                        #print('Imagen convertida a RGB')
                        image_obj.save(f'{img_cert[:-4]}.pdf')
                        print(f'Exportado a PDF. Archivo: {img_cert[:-4]}.pdf')
                        os.remove(img_cert)
                    except:
                        messagebox.showwarning('Problemas con el certificado!', 'No se generó el certificado. Revisa la configuración!')
                    else:
                        messagebox.showinfo('Certificado generado!', f'ID Predio: {cnt[0]}\nEstado: Certificado!\nArchivo: {img_cert[:-4]}.pdf')
                    break
        elif usr_npn.get():
            for id in d:
                np,est=d[id][5],d[id][1]
                if np == npn.lower().strip() and est not in ('8','9'):
                    #print(f'{np}={npn}|{id}={idPre}')
                    num+=1
                    cnt.insert(0,id)
                    cnt.insert(1,np)
                    cnt.insert(2,est)
                    #print(cnt)
            while True:
                if len(cnt) == 0:
                    messagebox.showwarning('Predio no encontrado!', 'NPN: {a} - Resultados: {b}\n \n¿Predio activo con estrato residencial?\nRevisa SIGCAT y Tipo Estrato'.format(a=npn,b=len(cnt)))
                    break
                else:
                    try:
                        messagebox.showinfo('Generando certificado!','Selecciona la plantilla .JPG!')
                        cert_plantilla=askopenfilename(filetypes=[('Imágenes','*.jpg')])
                        #print(cert_plantilla)
                        template=cv2.imread(cert_plantilla)
                        cv2.putText(template,f'{cnt[1]}',(2181,2525), cv2.FONT_HERSHEY_SIMPLEX,3.75,(0,0,0),16,cv2.LINE_AA)
                        cv2.putText(template,cnt[2],(1865,3035), cv2.FONT_HERSHEY_SIMPLEX,3.75,(0,0,0),16,cv2.LINE_AA)
                        cv2.putText(template,f'{strftime("%Y-%m-%d %H:%M:%S")}',(3580,4000), cv2.FONT_HERSHEY_SIMPLEX,3.75,(0,0,0),10,cv2.LINE_AA)
                        img_cert=os.path.join(os.path.dirname(cert_plantilla),fr'Certificado_{cnt[1]}.jpg')
                        cv2.imwrite(img_cert,template)
                        #print('Certificado en jpg')
                        image_obj = Image.open(img_cert).convert('RGB')
                        #print('Imagen convertida a RGB')
                        #image_obj.save(dire,fr'Certificado_{cnt[0]}.pdf')
                        image_obj.save(f'{img_cert[:-4]}.pdf')
                        print(f'Exportado a PDF. Archivo: {img_cert[:-4]}.pdf')
                        os.remove(img_cert)
                    except:
                        messagebox.showwarning('Problemas con el certificado!', 'No se generó el certificado. Revisa el valor ID Predio o NPN!')
                    else:
                        messagebox.showinfo('Certificado generado!', f'NPN: {cnt[1]}\nEstado: Certificado!\nArchivo: {img_cert[:-4]}.pdf')
                    break
        else:
            messagebox.showwarning('Sin resultados!', 'Ingresa un valor ID Predio o NPN!')
    except:
        messagebox.showwarning('Sin resultados!', 'No se pudo generar el certificado!')
    print("Certificación terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Función: generar reporte

def reporte():
    try:
        print("Reporte inició: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
        from matplotlib import pyplot

        # Servidor y conexión PostgreSQL
        con_sql()

        try:
            d_rep={}
            bd=bdm
            col_list = 'estestrato as estrato,count(*) as predios' # Columnas para la consulta SQL
            query = f"select {col_list} from {bd} group by estrato order by estrato;" # Query SQL
            #print(query)
            cursor_obj=con.cursor()
            cursor_obj.execute(query)
            for row in cursor_obj: # Row es igual al index de columnas en SQL Query
                estrato=row[0]
                predios=row[1]
                d_rep[estrato]=[predios] # Obtener los resultados de la consulta en diccionario
                continue # Cláusula para evitar copias repetidas
            cursor_obj.close()
            con.close()
        except:
            print('Consulta SQL: incorrecta')
        else:
            print('Consulta SQL: exitosa')     

        # Preparamiento de los datos

        estratos,predios,colores,explotar,pren=[],[],[],[],[]
        
        for a in d_rep:
            estratos.append(v(a))
            predios.append(d_rep[a][0])
            print(f'{v(a)} - Predios: {d_rep[a][0]}')
        
        for a in d5: colores.append(d5[a][1])
        for a in d5: explotar.append(d5[a][2])

        # Preparación del gráfico

        px = 1/pyplot.rcParams['figure.dpi']  # Convertir píxeles en pulgadas
        pyplot.subplots(figsize=(850*px, 550*px)) # Geometría
        pyplot.subplots_adjust(left=0.17, bottom=0.1)
        pyplot.style.use('ggplot')
        f_ti = {'family':'arial','color':'black'}
        pyplot.suptitle('Reporte base maestra de estratificación'.title(), fontdict=f_ti,fontsize=14) # fontweight='bold'
        #pyplot.title(f'Fecha: {strftime("%Y-%m-%d")} - Total predios: {sum(map(int, predios))}',fontdict=f_ti,fontsize=12)
        pyplot.text(x=-1,y=1.18,s=f'Fecha: {strftime("%Y-%m-%d")} - Total predios: {sum(map(int, predios))}',fontdict=f_ti,fontsize=12)
        pyplot.text(x=-1.89,y=1,s='Leyenda')
        pie = pyplot.pie(
            x=predios,
            colors=colores,
            explode=explotar,
            autopct='%1.1f%%',
            shadow=True,
            startangle=60,
            wedgeprops={'edgecolor':'black'}
            )
        pyplot.axis('equal')
        legend = pyplot.legend(estratos,loc='best', bbox_to_anchor=(0.099, 0.95))

        # Preparando tabla

        for a in predios: pren.append([a])
        pyplot.text(x=-1.95,y=-0.34,s='Tabla de datos')
        table = pyplot.table(
            cellText=pren,
            colWidths=[0.1] * 3,
            rowLabels=estratos,
            #colLabels="#",
            rowColours=colores,
            loc='lower left',
        )
        
        # Finalización

        print("Reporte terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
        messagebox.showinfo('Reporte realizado!', 'Reporte generado con éxito!')

        # Generar el gráfico

        pyplot.show(block=True)
    
    except:
        print('Problemas con el reporte')
        messagebox.showwarning('Reporte no realizado!', 'Problemas para generar el reporte!')

def historico():
    import webbrowser
    mLad=usr_mlad.get().strip().upper() # Variables
    if not usr_mlad.get() or len(mLad)!= 9:
        print('Sin resultados. Ingresa un valor Manzana-Lado!')
        messagebox.showwarning('Sin resultados!', 'Ingresa un valor Manzana-Lado!')
    elif usr_mlad.get() and len(mLad)==9:
        print("HISTÓRICO INICIÓ: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))
        try:
            mlad_his=f'http://idesc.cali.gov.co/servicios/estratificacion/historico.php?lado={mLad}'
            print(f'Buscando histórico para Manzana-Lado: {mLad}')
            messagebox.showinfo('Buscando estrato histórico!',f'Manzana - Lado: {mLad}\nNota: recuerda iniciar sesión en IDESC.')
            webbrowser.open(mlad_his)
            """web_historico = Toplevel(window) # Toplevel object which will be treated as a new window
            mapwin.title("Base Maestra de Estratificación - Mapa de localización") # sets the title of the Toplevel widget
            web_historico.geometry('800x600')
            webview.create_window('Estrato histórico de: {mLad}','https://idesc.cali.gov.co/geovisor.php')
            webview.start()"""
        except:
            print('PROBLEMAS CON EL ESTRATO HISTÓRICO')
            messagebox.showwarning('Histórico no realizado!', 'Problemas para generar el histórico!')
        else:
            print("HISTÓRICO terminó: ".upper() + strftime("%Y-%m-%d %H:%M:%S"))

# Recuadro # 4: información base maestra y fecha

fra_inf_bd = tkinter.LabelFrame(frameLeft,text='Información Base Maestra',font="TkDefaultFont 10")
fra_inf_bd.grid(row=0,column=3,sticky='nw',padx=20,pady=10)

lab_corte=tkinter.Label(fra_inf_bd,text=f'Corte: {ver} \nNúmero de registros: {nreg} \nFecha: {strftime("%Y-%m-%d")} \nHora: {strftime("%H:%M:%S")}',font="TkDefaultFont 9",justify=LEFT)
""" lab_reloj = tkinter.Label(frame, font="bahnschrift 8")
lab_reloj.place(x=750,y=560)
reloj() """
lab_corte.grid(row=0,column=0,sticky='sw',padx=10,pady=10)

# Recuadro # 4: desarrollado por
from PIL import ImageTk
from urllib.request import urlopen
fra_desa = tkinter.LabelFrame(frameLeft,text='Desarrollado por',font="TkDefaultFont 10")
fra_desa.grid(row=0,column=4,sticky='n',padx=15,pady=10)
#URL='https://onedrive.live.com/embed?resid=CD57FD321DC9167%2140596&authkey=%21ADLyZtejCSvRbu0&width=200&height=50'
url='https://drive.google.com/uc?export=view&id=15EpdrV8Won16saMU8Bz3He8FsN1S79zt'
u = urlopen(url)
raw_data = u.read()
u.close()
photo = ImageTk.PhotoImage(data=raw_data)
lab_corte=tkinter.Label(fra_desa,image=photo)
lab_corte.image = photo
lab_corte.grid(row=0,column=0,sticky='sw',padx=7,pady=4)

# Recuadro # 2: funciones oficina

fra_usr_funcion_oficina = tkinter.LabelFrame(frameLeft,text='Funciones Oficina',font="TkDefaultFont 10")
fra_usr_funcion_oficina.grid(row=0,column=1,sticky='nw',padx=20,pady=9)

# Recuadro # 2: funciones terreno

fra_usr_funcion_terreno = tkinter.LabelFrame(frameLeft,text='Funciones Terreno',font="TkDefaultFont 10")
fra_usr_funcion_terreno.grid(row=0,column=2,sticky='ne',padx=20,pady=9)

""" fra_usr_funcion_terreno = tkinter.LabelFrame(frameLeft,text='Funciones Terreno',font="TkDefaultFont 10")
fra_usr_funcion_terreno.grid(row=0,column=1,sticky='ne',padx=20,pady=9) """

# Recuadro # 2: limpiar

fra_usr_limpiar = tkinter.Frame(frameLeft)
fra_usr_limpiar.grid(row=0,column=2,sticky='s',padx=20,pady=9)

""" fra_usr_limpiar = tkinter.Frame(frameLeft)
fra_usr_limpiar.grid(row=0,column=1,sticky='s',padx=20,pady=9) """

# Botón buscar predio

bot_buscar=tkinter.Button(fra_usr_funcion_oficina,text='buscar predio'.title(),command=bus_predio,anchor='center',justify=LEFT,width=15,height=1,font="bahnschrift 11",fg="white",bg='#137fb0')
bot_buscar.grid(row=0,column=0,padx=10,pady=7)

# Botón localizar predio

bot_mapa=tkinter.Button(fra_usr_funcion_terreno,text='localizar predio'.title(),command=abrir_mapa,anchor='center',justify=CENTER,width=15,height=1,font="bahnschrift 11",fg="white",bg='#77a90c')
bot_mapa.grid(row=1,column=0,padx=10,pady=7)

# Botón ruta al predio

bot_cert=tkinter.Button(fra_usr_funcion_terreno,text='Ruta predio'.title(),command=ruta_predio,anchor='center',justify=CENTER,width=15,height=1,font="bahnschrift 11",fg="black",bg='#e3c5c3')
bot_cert.grid(row=2,column=0,sticky='nw',padx=10,pady=7)

# Botón limpiar consulta

bot_limp=tkinter.Button(fra_usr_limpiar,text='Limpiar consulta'.title(),command=limp,anchor='center',justify=CENTER,width=15,height=1,font="bahnschrift 11",fg="white",bg='#536270')
bot_limp.grid(row=2,column=0,sticky='nw',padx=10,pady=7)

""" bot_limp=tkinter.Button(fra_usr_limpiar,text='Limpiar consulta'.title(),command=limp,anchor='center',justify=CENTER,width=39,height=1,font="bahnschrift 11",fg="white",bg='#536270')
bot_limp.grid(row=2,column=0,sticky='nw',padx=10,pady=7) """

# Botón certificar predio

bot_cert=tkinter.Button(fra_usr_funcion_oficina,text='Certificar predio'.title(),command=cert,anchor='center',justify=CENTER,width=15,height=1,font="bahnschrift 11",fg="black",bg='#f2da99')
bot_cert.grid(row=2,column=0,sticky='nw',padx=10,pady=7)

# Botón historico

bot_cert=tkinter.Button(fra_usr_funcion_oficina,text='Estrato histórico'.title(),command=historico,anchor='center',justify=CENTER,width=15,height=1,font="bahnschrift 11",fg="black",bg='#bdcebe')
bot_cert.grid(row=1,column=0,sticky='nw',padx=10,pady=7)

# Botón generar reporte

bot_repor=tkinter.Button(fra_inf_bd,text='Generar reporte'.title(),command=reporte,anchor='center',justify=CENTER,width=15,height=1,font="bahnschrift 11",fg="white",bg='#2a9da1')
bot_repor.grid(row=1,column=0,sticky='s',padx=10,pady=7)

# Iniciar interfaz gráfica

window.resizable(False,False)
window.mainloop()