import hashlib

hash = '7f31162570de65864b2609fea2591524b2dcf9f84ce36161701f3ac6f467e95f'
ubicacion = input('Dirección del diccionario: ')

with open(ubicacion, 'r') as file:
    diccionario = [line.strip() for line in file]

    for password in diccionario:
        hash_calculado = hashlib.sha256(password.encode()).hexdigest()

        if hash_calculado == hash:
            print(f'La contraseña original es: {password}')
            break

        else:
            print('La contraseña no se encuentra en el diccionario')