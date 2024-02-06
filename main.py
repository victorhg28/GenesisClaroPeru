from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import datos

root = Tk()
root.title('Genesys')
##root.geometry("600x300")
root.config(pady=35,padx=35)

#20231006 IN


#archivos exportados
##inbound_resultado='IN.txt'
inbound_resultado='IN.txt'
outbound_resultado='OUT.txt'


#---- Funciones -------------------------------------------------------
def cortando_texto(ch1,ch2,my_str):
    return my_str[my_str.find(ch1)+1:my_str.find(ch2)]

#por si el usuario ingresa, por ejemplo, '5' en lugar de '05' en el día o mes 
def correccion_dia_o_mes(cadena):
    if(len(cadena)==1):
        return ('0'+cadena)
    else:
        return cadena

#adaptando la fecha al formato de fecha del reporte
def formato_fecha(x_año,x_dia,x_mes):
    return (''+x_año+x_mes+x_dia)

#para reportes IN: 662,cd001,79,cdrivr,1537,1297
def formato_fecha_2(x_año,x_dia,x_mes):
    return (''+x_dia+x_mes+x_año)

def creacion_salida():
    f = open(inbound_resultado, "w")
    f.write("############\n")
    f.write("RESULTADOS INBOUND\n")
    f.write("############\n")
    f.write("\n")
    f.close()

    f = open(outbound_resultado, "w")
    f.write("############\n")
    f.write("RESULTADOS OUTBOUND\n")
    f.write("############\n")
    f.write("\n")
    f.close()

def exportar_existe(nom_archivo,tamaño,nom_file_export,t_fixed):
    f = open(nom_file_export, "a")
    f.write("\n")
    f.write(nom_archivo)
    f.write("\ttamaño(bytes):")
    f.write(tamaño)
    f.write("\t")
    if(int(tamaño)<=t_fixed):
        f.write("estado: SIN_DATOS")
    else:
        f.write("estado: OK")
    f.close()
    print(str(t_fixed))

def salto_de_linea():
    f = open("matriz_reportes_genesys.txt", "a")
    f.write("\n")
    f.close()

def exportar_no_existe(nom_archivo,nom_file_export):
##    print("se ejecutó")
    f = open(nom_file_export, "a")
    f.write("\n")
    f.write(nom_archivo)
    f.write("\ttamaño(bytes):")
    f.write("NO EXISTE")
    f.write("\t")
    f.write("estado: NO EXISTE")
    f.close()
			

def seleccionar_global():
    print('iniciado')
    creacion_salida()

    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
##  archivo_seleccionado.config(text = filename,bg="green",fg="white")
    archivo_seleccionado.config(text = filename,bg="green",fg="white")

    #activando boton ejecutar una vez que se ha seleccionado el archivo
    boton_ejecutar.config(state='normal')


    
def ejecutar():
    filename = archivo_seleccionado['text']
    
##    for y in datos.array_INBOUNDS:
##        for x in y:
##            select_file(x,filename)
##            
##    for z in datos.array_OUTBOUNDS:
##        for c in z:
##            select_file_2(c,filename)


##  para nuevo dianmico fx
##    mode = True
    
    for y in datos.array_INBOUNDS:
        for x in y:
            iteracion(x,filename,True)
            
    for z in datos.array_OUTBOUNDS:
        for c in z:
            iteracion(c,filename,False)

    print("terminado")
    archivo_seleccionado.config(bg="green",fg="white")
    

##para IN
def iteracion(excel,filename,mode):
    
    word=''
    reporte_nom=''
    fecha_temp=''

    if(mode): #IN
        file_nombre_aux=inbound_resultado
    else: #OUT
        file_nombre_aux=outbound_resultado


    with open(filename, 'r') as fp:
        # leyendo todas la lineas usando readline()
        lines = fp.readlines()
        resultado_busqueda = 0
        
        for row in lines:
            # verifica si string se encuentra en la línea actual
            if("[" in row):
                reporte_nom = cortando_texto("[","]",row)
##                print(reporte_nom)
                if(mode): #IN
                    if(reporte_nom=='194' or reporte_nom=='90' or reporte_nom=='89' or reporte_nom=='1717'):
                        fecha_temp=formato_fecha(entry_año.get(),correccion_dia_o_mes(entry_dia.get()),correccion_dia_o_mes(entry_mes.get()))
                    elif (reporte_nom=='662' or reporte_nom=='CD001' or reporte_nom=='79' or reporte_nom=='CDRIVR' or reporte_nom=='1537' or reporte_nom=='1297'):
                        fecha_temp=formato_fecha_2(entry_año.get(),correccion_dia_o_mes(entry_dia.get()),correccion_dia_o_mes(entry_mes.get()))
                else: #OUT
                    fecha_temp=formato_fecha(entry_año.get(),correccion_dia_o_mes(entry_dia.get()),correccion_dia_o_mes(entry_mes.get()))
  
            word = excel[0]
            word = word + fecha_temp

            resultado_busqueda = row.find(word)
                
            # metodo "find()" retorna -1 si el valor no se ha encontrado,
            #si lo encuentra devuelve el indice de la primera ocurrencia del substring
            if row.find(word) != -1: 
                resultado=row[21:39].replace(" ", "")
                resultado=resultado.replace(",", "")
                print(word)
                exportar_existe(word,resultado,file_nombre_aux,excel[1])
                break
                
        if resultado_busqueda == -1:
            exportar_no_existe(word,file_nombre_aux)




#---- Fecha -------------------------------------------------------

#Entries_INBOUND
str_año='2023'
label_año = Label(text = "INBOUND año: ")
entry_año = Entry(textvariable=str_año)

str_mes=''
label_mes = Label(text = "INBOUND mes: ")
entry_mes = Entry(textvariable=str_mes)

str_dia=''
label_dia = Label(text = "INBOUND dia: ")
entry_dia = Entry(textvariable=str_dia)


#Entries_OUTBOUND
str_año_OUT='2023'
label_año_OUT = Label(text = "OUTBOUND año: ")
entry_año_OUT = Entry(textvariable=str_año_OUT)

str_mes_OUT=''
label_mes_OUT = Label(text = "OUTBOUND mes: ")
entry_mes_OUT = Entry(textvariable=str_mes_OUT)

str_dia_OUT=''
label_dia_OUT = Label(text = "OUTBOUND dia: ")
entry_dia_OUT = Entry(textvariable=str_dia_OUT)

label_separador = Label(text = "-----------------------------------------------------")


#---- Elementos GUI -------------------------------------------------------

# Labels
archivo_seleccionado = Label(text = "*ningun archivo abierto*",bg="red",fg="white")

# Botones
open_button = Button(
    root,
    text='Abrir archivo',
    command=seleccionar_global
)

boton_ejecutar = Button(
    root,
    text='Ejecutar',
    state=DISABLED,
    command=ejecutar
)

#Separadores
styl = ttk.Style()
styl.configure('blue.TSeparator', background='black')
mi_separador = ttk.Separator(
    master=root,
    orient=HORIZONTAL,
    style='blue.TSeparator',
    class_= ttk.Separator,
    takefocus= 1,
    cursor='plus'    
)
mi_separador_2 = ttk.Separator(
    master=root,
    orient=HORIZONTAL,
    style='blue.TSeparator',
    class_= ttk.Separator,
    takefocus= 1,
    cursor='plus'    
)


# variables para colocar elementos de GUI en la grid
indice_col = 0
indice_row = 0

# Poniendo elementos graficos en grid
open_button.grid(row = indice_row, column = indice_col, pady = 2)
archivo_seleccionado.grid(row = indice_row, column = indice_col+1, pady = 2)
indice_row+=1

mi_separador.grid(row=indice_row, columnspan=2, ipadx=200, pady=10)
indice_row+=1

label_año.grid(row = indice_row, column = 0, pady = 2)
entry_año.grid(row = indice_row, column = 1, pady = 2)
indice_row+=1

label_mes.grid(row = indice_row, column = 0, pady = 2)
entry_mes.grid(row = indice_row, column = 1, pady = 2)
indice_row+=1

label_dia.grid(row = indice_row, column = 0, pady = 2)
entry_dia.grid(row = indice_row, column = 1, pady = 2)
indice_row+=1

mi_separador_2.grid(row=indice_row, columnspan=2, ipadx=200, pady=10)
indice_row+=1

label_año_OUT.grid(row = indice_row, column = 0, pady = 2)
entry_año_OUT.grid(row = indice_row, column = 1, pady = 2)
indice_row+=1

label_mes_OUT.grid(row = indice_row, column = 0, pady = 2)
entry_mes_OUT.grid(row = indice_row, column = 1, pady = 2)
indice_row+=1

label_dia_OUT.grid(row = indice_row, column = 0, pady = 2)
entry_dia_OUT.grid(row = indice_row, column = 1, pady = 2)
indice_row+=1


boton_ejecutar.grid(row = indice_row, columnspan=2, ipadx=200, pady=10)

# poniendo años por defecto
entry_año.delete(0,END)#entry año a "2023" por defecto
entry_año.insert(0,2023)#entry año a "2023" por defecto
entry_año_OUT.delete(0,END)#entry año a "2023" por defecto
entry_año_OUT.insert(0,2023)#entry año a "2023" por defecto

#---- Main Loop -------------------------------------------------------
root.mainloop()

