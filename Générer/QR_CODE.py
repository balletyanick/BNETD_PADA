import qrcode  # type: ignore

# URL avec niveau de zoom
url = "http://192.168.137.33:8000/00212P11789/"                                       

# Création de l'objet QRCode
qr = qrcode.QRCode(
    version=1,  # Version du code QR (1 à 40, 1 étant la plus petite)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Niveau de correction d'erreur (L, M, Q, H)
    box_size=10,  # Taille de chaque "boîte" du code QR
    border=4,  # Marge autour du code QR
)

# Ajout de l'URL au code QR
qr.add_data(url)
qr.make(fit=True)

# Création de l'image du code QR
img = qr.make_image(fill_color="MidnightBlue", back_color="white")

# Enregistrement de l'image du code QR
img.save("local.png")