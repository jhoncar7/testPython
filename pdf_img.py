import imgkit
import pdfkit
import jinja2
import os
import uuid
import base64


def crear_img(ruta_template, info, rutacss=''):

    nombre_templat = ruta_template.split('/')[-1]
    ruta_template = ruta_template.replace(nombre_templat, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(nombre_templat)
    html = template.render(info)

    path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)

    kitoptions = {
        "enable-local-file-access": None,
    }
    
    id_img = uuid.uuid4().hex

    path_file_new = os.path.abspath('./') + '/static/img/comunicados/' + f'{id_img}.jpg'
    
    imgkit.from_string(config=config, output_path=path_file_new,string=html, css=rutacss, options=kitoptions)

    image = open(path_file_new, 'rb')  # open binary file in read mode
    image_read = image.read()
    image_64_encode = str(base64.b64encode(image_read))
    cadena = image_64_encode.lstrip("b'")
    cadena = cadena.rstrip("'")
    vista_previa = (f"http://127.0.0.1:5000/vista-previa/{id_img}.jpg")
    return {id_img, vista_previa, cadena}


def crea_pdf(ruta_template, info, ruta_css=''):

    nombre_templat = ruta_template.split('/')[-1]
    ruta_template = ruta_template.replace(nombre_templat, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(nombre_templat)
    html = template.render(info)

    config = pdfkit.configuration(
        wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    nombre = 'pdf_creado.pdf'

    pdfkit.from_string(configuration=config,
                       output_path=nombre, input=html, css=ruta_css)


if __name__ == '__main__':
    ruta_template = os.path.abspath('./')+'/templates/it_comunica_cortes.html'
    # ruta_template = os.path.abspath('./')+'/it_comunica_cortes.html'
    # ruta_template = os.path.abspath('./')+'/index.html'
    ruta_css = os.path.abspath('./')+'/static/css/cortes.css'
    # ruta_css = os.path.abspath('./')+'/cortes.css'
    # ruta = 'C:/Users/ad125615/Documents/Desarrollos_AD/Bot-Comunicados/Api_Flask/index.html'
    info = {
        'title': 'Jhon',
        'description': 'Car'
    }
    # crea_pdf(ruta_template, info)
    crear_img(ruta_template, info, ruta_css)
