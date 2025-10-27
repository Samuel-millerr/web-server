from core.authentication.authentication import Authentication as auth
usuario = {
    "id": 1,
    "role": "comum",
}

print(auth.generate_token(usuario))

usuario = {
    "id": 2,
    "role": "administrador",
}

print(auth.generate_token(usuario))