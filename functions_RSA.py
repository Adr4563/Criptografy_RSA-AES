import random
import math
from PIL import Image
import csv
from datetime import datetime

csv_file_cifrado = './C_and_D_png/cifrado.csv'
csv_file_descifrado = './C_and_D_png/descifrado.csv'

#*************** Others Methods ******************#
# Calculate n & phi_n
def calculate_module(p,q):
    return p*q,(p - 1) * (q - 1)

# Private Key       
def mod_inverse(e, phi_n):
    
    for d in range(3, phi_n):
        if (d * e) % phi_n == 1:
            return d
    raise ValueError("mod_inverse doesn't exist")

# Publick Key
def generate_public_key(phi_n):
    # Genera una clave pública e aleatoria tal que 1 < e < phi_n y gcd(e, phi_n) = 1.
    e = random.randint(3, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)
    return e

#************************************************#




#***************Numbers Primes*******************#
# Numbers Primes
def generate_prime(max):
    while True:
        num = random.randint(1, max)
        if is_prime(num):
            return num
        
# Verify if the number is prime
def is_prime(num):    
    if num < 2 or num % 2 == 0:
        return False
    if num == 2:
        return True
    
    for d in range(3, int(math.sqrt(num)) + 1):
        if num % d == 0:
            return False
    return True

# Verify if the primes are diferentes between P & Q
def generate_different_primes(max):
    p, q = generate_prime(max), generate_prime(max)
    # P & Q are diferents
    while p == q:
        q = generate_prime(max)
    return p, q

#**********************************************#


#*************** Cipher Message ***************#
def rsa_cipher(message, e, n):
        ciphertext = []
        for char in message:
            # Characters ASCII
            char_code = ord(char)
            encrypted_char = pow(char_code, e, n)
            ciphertext.append(encrypted_char)

        return ciphertext

def rsa_decoded(ciphertext, d, n):
    decipher_text = []
    for encrypted_char in ciphertext:
        dechipher_char_code = pow(encrypted_char, d, n)
        decrypted_char = chr(dechipher_char_code)
        decipher_text.append(decrypted_char)            
    return "".join(decipher_text)
#***********************************************#


#*************** Cipher File TXT ***************#
def cipher_txt(input_file, output_file, e, n):
    
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        
    ciphertext = rsa_cipher(content, e, n)

    with open(output_file, 'w', encoding='utf-8') as file:
        for char_code in ciphertext:
            file.write(str(char_code) + ' ')
    print(f"Archivo TXT cifrado se guarda en {output_file}")

def decipher_txt(input_file, output_file, d, n):
    with open(input_file, 'r', encoding='utf-8') as file:
        ciphertext = file.read().split()
        ciphertext = [int(code) for code in ciphertext]

    decoded_message = rsa_decoded(ciphertext, d, n)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(decoded_message)
    print(f"Archivo TXT descifrado se guarda en {output_file}")

#*********Images Format (PNG/JPG)***************#

def cipher_image(input_image, output_image, e,n):
    image = Image.open(input_image)
    pixels = list(image.getdata())
    # print(pixels)     : [(255,255,255),....]
    # print(image.size) : RGBA (255,255,255,255) ||  RGB (255,255,255)
    cipher_pixels = []
    
    data = []
    id = 0
    for pixel in pixels:
        list_pixel = []
        timestamp = datetime.now().strftime("%H:%M:%S")
        for value in pixel:
            cipher_value = pow(value, e, n)  
            list_pixel.append(cipher_value)
        
        if len(pixel) == 4:
            color = ['Red', 'Green', 'Blue', 'Alpha'][id % 4] 
        else:
            color = ['Red', 'Green', 'Blue'][id % 3]
        
        data.append([timestamp, color, pixel, tuple(list_pixel)])
            
        cipher_pixels.append(tuple(list_pixel )) # Primer segmento de pixeles de la fila n
        #  Calculatar el cipher_value
        #  Public key = 659447
        #  Example: (255,100,255) => (255**Public-Key[0]) mod public_key[1]
        #  (255,100,255) => (255**6) mod 5
        #  (255,100,255) => (100**6) mod 5
        id = id + 1
        
    # print(cipher_pixels) : [(255,255,255,255)......]
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(cipher_pixels)
    new_image.save(output_image)     
    print(f"Imagen cifrada se guarda en:  '{output_image}'")
    
    # Data to CSV
    with open(csv_file_cifrado, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["TimeStamp", "Color", "Pixel_Value", "Ciphered_Value"])
        writer.writerows(data)

    print(f"Datos de cifrado guardados en: '{csv_file_cifrado}'")

def decoded_image(input_image, output_image, d, n):
    cipher_image = Image.open(input_image)
    cipher_pixels = list(cipher_image.getdata())
    decoded_pixels = []
    data = []
    id = 0
    for pixel in cipher_pixels:
        timestamp = datetime.now().strftime("%H:%M:%S")
        list_pixel = []
        id = 0
        for value in pixel:
            decoded_value = pow(value, d, n)
            list_pixel.append(decoded_value)
        if len(pixel) == 4:
            color = ['Red', 'Green', 'Blue', 'Alpha'][id % 4] 
        else:
            color = ['Red', 'Green', 'Blue'][id % 3]
        data.append([timestamp, color, pixel, tuple(list_pixel)])
        
        decoded_pixels.append(tuple(list_pixel))
        id = id + 1 

    new_image = Image.new(cipher_image.mode, cipher_image.size)
    new_image.putdata(decoded_pixels)
    new_image.save(output_image)
    print(f"Imagen descifrada se guarda en: '{output_image}'")
    
    # Data to CSV
    with open(csv_file_descifrado, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["TimeStamp", "Color", "Pixel_Value", "Decoded_Values"])
        writer.writerows(data)
    
    print(f"Datos de descifrado guardados en: '{csv_file_descifrado}'")
#***********************************************#
def results():
    max = int(input("Ingresar tamaño (bits): "))
    p, q = generate_different_primes(max)
    print(f"p {p} and  q {q}")
    
    # Calculate n and phi_n     
    n, phi_n = calculate_module(p,q)
    print(f"n {n} and  phi_n :{phi_n}")
    
    # Public Key
    e = generate_public_key(phi_n)
    print(f"Public key: {e}")
    
    # Private Key
    d = mod_inverse(e, phi_n)
    print(f"Public key: {d}")
    
    #***************** Message to Cipher ***************************************************#
    message = "HOLA MUNDO"
    
    ciphertext = rsa_cipher(message, e, n) # We need the Public Key & the module n
    print(f"cipher message:{ciphertext}")   

    decoded_text  = rsa_decoded(ciphertext, d, n) # We need the Private Key & the module n
    print(f"cipher message: {decoded_text}") 
    #***************************************************************************************#
    
    #***************** File TXT to Cipher **************************************************#
    cipher_txt('./C_and_D_txt/archivo_html.txt', './C_and_D_txt/resultados/cifrado.txt',  e, n)
    decipher_txt('./C_and_D_txt/resultados/cifrado.txt', './C_and_D_txt/resultados/descifrado.txt', d, n)
    
    #**************************************************************************************#
    
    #**************** Image to Cipher Format(PNG/JPG/GIF) *********************************#
    cipher_image('./C_and_D_png/box.png', './C_and_D_png/resultados/cifrado.png', e, n)
    decoded_image('./C_and_D_png/resultados/cifrado.png', './C_and_D_png/resultados/descifrado.png', d,n)
    
    #**************************************************************************************#
      
      
results()