from clases.RNA_Allocator import RNA_Allocator
import base64

rna_alloc = RNA_Allocator()

def get_ultimo_objeto_on_train(account):
    red = rna_alloc.getRNA(account.id)
    return red.last_obj_on_train

def is_on_training(account):
    red = rna_alloc.getRNA(account.id)
    return (red.getEstado() == 'ON_TRAINING')

def imagen_a_base64(ruta_de_la_imagen):
    try:
        with open('storage/'+ ruta_de_la_imagen, "rb") as image_file:
            # Lee la imagen en bytes
            image_data = image_file.read()
            
            # Codifica la imagen en Base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Devuelve la imagen codificada en Base64 como respuesta JSON
            return base64_image
    except FileNotFoundError:
        return 'error'

def base64_a_imagen(string_base_64):
    binary_data = base64.b64decode(string_base_64.encode())
    return binary_data
