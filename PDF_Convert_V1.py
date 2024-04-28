######################### LIBRERIAS #########################
import os
import time
from pdf2image import convert_from_path
from PIL import Image
from pypdf import PdfWriter,PdfReader
#############################################################

poppler_path = #COLOCA LA RUTA DE TU POPPLER

# Limpiar consola
def clearConsole():
    """Limpia la consola (funciona solo en Windows)"""
    os.system('cls')

# Convertir PDF a Imagen (JPG y PNG)
def pdf_to_image_all(file_path,file_name,dpi=300):
    """
    Convierte todas las páginas de un PDF a imágenes JPG o PNG.
    Args:
        file_path (str): Ruta del archivo.
        file_name (str): Nombre del PDF.
        dpi (int): DPI de la imagen (predeterminado: 300).
    """
    file = os.path.join(file_path, file_name + ".pdf") #Ruta completa de archivo
    images = convert_from_path(file, dpi=dpi,poppler_path=poppler_path) #Convertir todo el PDF a imágenes con un DPI predeterminado
    
    for idx,image in enumerate(images):
        image.save(os.path.join(file_path, f"{file_name}_{idx}.png"),'PNG')
    
    print("######### Convertiste todos las hojas de un documento PDF a imágenes y se guardaron en "+ file_path+" #########")

def pdf_to_image_foreach(file_path,file_name,page=None,dpi=300):
    """
    Convierte todas las páginas de un PDF a imágenes JPG o PNG.
    Args:
        file_path (str): Ruta del archivo.
        file_name (str): Nombre del PDF.
        page (int, opcional): Número de página para convertir (predeterminado: None).
        dpi (int): DPI de la imagen (predeterminado: 300).
    """
    try:
        file = os.path.join(file_path, file_name + ".pdf") #Ruta de archivo
        images = convert_from_path(file, dpi=dpi,poppler_path=poppler_path)
 
        if page is not None:
            i = int(page-1)
            images[i].save(os.path.join(file_path, f"{file_name}_{str(i+1)}.png"),'PNG')
            clearConsole()
            print(f"######### Convertiste la página {page} del archivo '{file_name}' a una imagen y se guardo en {file_path} #########")
        else:
            print("Error: Tienes que seleccionar una página")
    except:
        clearConsole()
        print(f"¡Error!\nIntentaste convertir la página {page}, este PDF solo tiene {len(images)} páginas")
        
# Convertir Imagen a PDF
def image_to_pdf_foreach(file_path,file_name):
    """Convierte una imagen (PNG, JPG, JPEG) a PDF
        Args:
        file_path (str): Ruta del archivo.
        file_name (str): Nombre del PDF.
    """
    while True:
        try:
            ext = int(input("1.PNG\n2.JPG\n3.JPEG\nIngresa el formato de tu imagen: "))
            route = os.path.join(file_path,file_name)
            extensions = {
                1: ".png",
                2: ".jpg",
                3: ".jpeg"
            }
            extension = extensions.get(ext)

            if extension: #De acuerdo con el valor obtenido
                print(f"Estás editando el documento {route+extension}")
                image = Image.open(route + extension)
                image.save(route+".pdf","PDF",resolution=100.0, save_all=True)
                break
            else:
                print("Opción inválida")
        except ValueError:
            print("Opción inválida")

# Unir varias imágenes en PDF
def image_to_pdf_all(file_path):
    """
    Convierte varias imágenes en un solo PDF
        Args:
        file_path (str): Ruta del archivo.
    """
    try:
        files = os.listdir(file_path)
        nombre = os.path.splitext(os.path.basename(files[0]))[0]
        img_list = []

        for file in files:
            archivo = os.path.join(file_path,file)
            img = Image.open(archivo)
            img_list.append(img)

        img_list[0].save(os.path.join(file_path,nombre+'.pdf'),
                     save_all = True,
                     append_images=img_list[1:]) #Save no guarda str, sino primero tenemos que abrirlos como formato de imagen.
    except:
        clearConsole()
        print("En esta ruta no hay imágenes de algún formato")
    
# Unir PDF
def mergePDF(file_path):
    """
        Convierte múltiples PDF en un solo PDF
        Args:
        file_path (str): Ruta del archivo.
    """
    try:
        files = os.listdir(file_path)
        merger = PdfWriter()

        for file in files:
            path = os.path.join(file_path, file)
            merger.append(path)

        output_file = os.path.join(file_path,'merged.pdf')
        merger.write(output_file)
        merger.close()
        print(f"Se unió el documento en: {output_file}")
    except:
        clearConsole()
        print("¡Ha ocurrido un error! La ruta no es válida")

# # Separar PDF
def splitPDF(file_path,file_name):
    """Separa un PDF en varios PDF pequeños
        Args:
        file_path (str): Ruta del archivo.
        file_name (str): Nombre del PDF.
    """
    input_file = os.path.join(file_path, file_name + ".pdf") #Ruta de archivo
    output_path = os.path.join(file_path)

    with open(input_file, 'rb') as file: #Abres el archivo en modo lectura
        pdf_reader = PdfReader(file) #Usas el lector para abrir el archivo
        
        for page_num in range(pdf_reader.get_num_pages()):
            output_page = os.path.join(output_path,f"{file_name}_{page_num+1}.pdf")
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.get_page(page_num))

            with open(output_page, 'wb') as output_file:
                pdf_writer.write(output_file)

########## PROGRAMA ##########
clearConsole()
print (f"#"*32+"\n###Created by renzo-plasencia###\n"+"#"*32)
#print("################################\n###Created by renzo-plasencia###\n""#"" * 32
time.sleep(2)
clearConsole()

def pdfMain():
    dpi = 300
    while True:
        #clearConsole()
        print("#################### Menú ####################")
        print("1.PDF to Image\n2.Image to PDF\n3.Merge PDF\n4.Split PDF\n5.Exit")
        try:
            opcion = int(input("Ingresa una opción: "))
            if opcion == 1:
                print("########### PDF to Image ###########")
                file_path = str(input("Ingresa ruta: "))
                file_name = str(input("Ingresa archivo: "))
                print(f"Estas editando el documento: {os.path.join(file_path,file_name+".pdf")}")
                print("1.Convertir todas las páginas\n2.Convertir una página\n3.Cambiar DPI\n4.Menú principal")
                opcion1 = int(input("Elige una opción: "))
                if opcion1 == 1:
                    try:
                        pdf_to_image_all(file_path,file_name)
                    except:
                        clearConsole()
                        print("Revisa la ruta")
                    
                elif opcion1 == 2:
                    try:
                        pagina = int(input("Ingresa página:"))
                        pdf_to_image_foreach(file_path,file_name, pagina)
                    except:
                        clearConsole()
                        print("Error reivsa tu ruta o la página")

                elif opcion1 == 3:
                    dpi = int(input("Ingresa DPI:"))
                    print("Cambiaste el DPI de la imagen resultante a "+dpi)
                    
                elif opcion1 == 4:
                    break

                else: 
                    print("Opción inválida")

            elif opcion == 2:
                clearConsole()
                print("########### Image to PDF ###########")
                file_path = str(input("Ingresa ruta: "))
                opcion2 = int(input("1.Una imagen a PDF\n2.Varias imágenes a PDF\n3.Menú principal\nIngresa opción: "))

                if opcion2 == 1:
                    try:
                        file_name = str(input("Ingresa archivo:"))
                        image_to_pdf_foreach(file_path,file_name)
                    except:
                        clearConsole()
                        print("¡Ha ocurrido un error! Ingresa la ruta correcta.")
                elif opcion2 == 2:
                    image_to_pdf_all(file_path)

                elif opcion2 == 3:
                    break
                else:
                    print("Opción inválida")

            elif opcion == 3:
                clearConsole()
                print("########### Merging PDF ###########")
                file_path = str(input("Ingresa ruta:"))
                mergePDF(file_path)

            elif opcion == 4:
                clearConsole()
                print("####Split PDF####")
                try:
                    file_path = str(input("Ingresa ruta:"))
                    file_name = str(input("Ingresa archivo:"))
                    splitPDF(file_path,file_name)
                    print("Se separó el documento satisfactoriamente")
                except:
                    clearConsole()
                    print("¡Ha ocurrido un error! Revisa la ruta o el nombre del archivo")
    
            elif opcion == 5:
                break

            else:
                clearConsole()
                print("Opción inválida")
        except ValueError:
            clearConsole()
            print("Opción inválida")


pdfMain()
