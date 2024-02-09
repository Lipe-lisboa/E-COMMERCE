from pathlib import Path

from django.conf import settings
from PIL import Image
import re

def resize_image(image_django, new_width=800, optimize=True, quality=60):
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()
    img = Image.open(image_path)
    original_width, original_height = img.size

    if original_width <= new_width:
        img.close()
        return img

    
    #regra de 3
    new_height = round(new_width * original_height / original_width)

    new_image = img.resize((new_width, new_height), Image.LANCZOS)

    new_image.save(
        image_path,
        optimize=optimize,
        quality=quality,
    )

    return new_image


def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11:
        return False

    novo_cpf = cpf[:-2]                 # Elimina os dois últimos digitos do CPF
    reverso = 10                        # Contador reverso
    total = 0

    # Loop do CPF
    for i in range(19):
        if i > 8:                   # Primeiro índice vai de 0 a 9,
            i -= 9                  # São os 9 primeiros digitos do CPF

        total += int(novo_cpf[i]) * reverso  # Valor total da multiplicação

        reverso -= 1                    # Decrementa o contador reverso
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d > 9:                   # Se o digito for > que 9 o valor é 0
                d = 0
            total = 0                   # Zera o total
            novo_cpf += str(d)          # Concatena o digito gerado no novo cpf

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Descobri que sequências avaliavam como verdadeiro, então também
    # adicionei essa checagem aqui
    if cpf == novo_cpf and not sequencia:
        return True
    else:
        return False


def valida_cep(cep):
    list_number = ['0','1','2', '3', '4', '5', '6', '7', '8', '9']
    
    for i in cep:
        if i not in list_number:
            return False
    
    if len (cep) > 8 or len (cep) < 8 :
         return False
     
    return True