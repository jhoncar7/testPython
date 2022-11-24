from flask import Flask, request, render_template
from pdf_img import crear_img
import os

app = Flask(__name__)


@app.get('/')
def get_comunicado():
    return {"status": True}


@app.post('/api/it_comunica_cortes')
def it_comunica_cortes():
    try:
        data = request.get_json()
        keys = data.keys()

        if 'title' in keys and 'description' in keys:

            ruta_template = os.path.abspath(
                './')+'/templates/it_comunica_cortes.html'
            ruta_css = os.path.abspath('./')+'/static/css/cortes.css'

            [id_img, vista_previa, cadena] = crear_img(
                ruta_template, data, ruta_css)

            return {'status': True, 'id_img': id_img, 'vista_previa': vista_previa, "cadena": str(cadena)}, 201
        return {'status': False, 'msg': 'Enviar los parametros [title y description]'}, 404

    except KeyError:
        return {'status': False, 'msg': 'Ocurrio un error inesperado'}, 500


@app.route('/vista-previa/<string:id_img>')
def vista_previa(id_img):
    existe = os.path.exists(os.path.abspath('./')+f'/static/img/comunicados/{id_img}')
    if existe:
        return render_template('vista_previa.html',id_img=id_img)
    else:
        return render_template('no_found.html')
