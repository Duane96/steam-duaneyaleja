from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from io import BytesIO

def generar_pdf(participante, campo_qr):
    # Crea un objeto de respuesta que será el PDF.
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Añade el membrete al PDF.
    p.setFont("Helvetica-Bold", 20)
    p.drawString(230, 700, "Duane y Aleja STEAM")  # Ajusta las coordenadas según tus necesidades

    # Añade el título al PDF.
    p.setFont("Helvetica-Bold", 16)
    p.drawString(80, 650, "Te damos la bienvenida a nuestro Intensivo: Más Sensual")  # Ajusta las coordenadas según tus necesidades

    # Dibuja el código QR en el PDF.
    imagen_qr = Image.open(getattr(participante, campo_qr).path)
    imagen_qr.thumbnail((200, 200))  # Ajusta el tamaño del código QR
    p.drawInlineImage(imagen_qr, 80, 400)  # Ajusta las coordenadas según tus necesidades

    # Añade un párrafo al PDF.
    p.setFont("Helvetica", 12)
    p.drawString(80, 350, "Este es tu pase de entrada a nuestro evento, no olvides llevarlo.")  # Ajusta las coordenadas según tus necesidades

    # Añade más texto al PDF.
    p.setFont("Helvetica", 12)
    p.drawString(80, 300, "Recuerda llegar puntual el día del evento. Cualquier duda, por favor no dude en contactarnos.")  # Ajusta las coordenadas según tus necesidades

    # Finaliza la página y guarda el PDF.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
