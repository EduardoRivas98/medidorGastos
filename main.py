from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
from io import BytesIO
from connect import cnx
from datetime import datetime

app = FastAPI()

# HTML que se muestra
# html_form = """
# <form method="post" enctype="multipart/form-data" action="/uploadfile/">
#     <label for="file">Subir CSV: </label>
#     <input type="file" name="file" accept=".csv">
#     <input type="submit">
# </form>
# """

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))
    
    #arreglo que almacenara los datos
    informacion_almacenados = []
    #for que recorre el indice y la fila.
    for indice, fila in df.iterrows():
        monto = fila["Monto"]
        ingreso = fila["Ingreso"]
        fecha_str = fila["Fecha"]

        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S")

        tipo_ingreso = fila["Tipo Ingreso"]

        #abre el arreglo y mete los objetos de datos
        informacion_almacenados.append({"indice":indice, "monto":monto, "ingreso":ingreso, "fecha":fecha, "tipo_ingreso":tipo_ingreso})
    
    #Se insertara a la BD
    try:
        with cnx.cursor() as cursor:
            query = "INSERT INTO ingresosDatos (monto, ingreso, fecha, tipo_ingreso) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (monto, ingreso, fecha, tipo_ingreso))
        cnx.commit()
    except Exception as e:
            return {"message": f"Error al insertar en la base de datos: {str(e)}"}

    
    return {"filename": file.filename, "rows": len(df), "info": informacion_almacenados}

#verificar que recibo la info
# @app.get("/form/")
# async def form_post():
#     return HTMLResponse(content=html_form, status_code=200)
