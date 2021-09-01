import argparse
import datetime
import django
import os
import sys
import time
import threading
import traceback

import cv2
import imutils
from imutils.video import VideoStream
from PIL import Image, ImageTk
from pyzbar import pyzbar
import tkinter as tk
from tkinter import messagebox


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clearning.settings')
django.setup()


from modules.attendances.models import Attendance
from modules.students.models import Student
from modules.teachers.models import Teacher
from modules.courses.models import (
    Course, CourseOpening, Enrollment
)


class UIMarcajeAsistencia(tk.Frame):

    hilo = None
    cuadro = None
    terminado = False
    panelVideo = None

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.curso = Course.objects.filter().first()
        
        if not self.curso:
            print("No existe el curso de Programación en Python")
            sys.exit(-1)

        # Obtener apertura del curso
        self.opening = CourseOpening.objects.filter(course=self.curso).first()

        self.parent = parent
        self.camara = VideoStream(usePiCamera=False).start()

        self.hilo = threading.Thread(target=self.cicloVideo, args=())
        self.hilo.start()

        self.parent.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        time.sleep(.5)
        self.init_ui()


    def init_ui(self):
        titulo_qr = tk.Label(
            self.parent, text="Presente su carnet para escanear el codigo QR\n y poder ingresar al aula",
            font=("Verdana", 12))

        titulo_curso = tk.Label(
            self.parent, text="Curso de \nIntroducción a la Programación \nen Python",
            font=("Verdana", 20, "bold"), height=18, width=16)

        titulo_qr.config(bg="#FFFFFF")
        titulo_curso.config(bg="#51d1f6")
        titulo_curso.config(fg="#FFFFFF")

        titulo_curso.pack(side="right", fill="both", expand="yes", padx=10, pady=0)
        titulo_qr.pack(side="bottom", padx=10, pady=20)


    def autenticacionExitosa(self, title="Autenticación exitosa", message=""):
        top = tk.Toplevel()
        top.title(title)
        top.geometry("420x180")
        tk.Label(top, text=message, font=("Verdana", 12), padx=2, pady=2).pack(
            side="top", fill="both", expand="yes"
        )
        top.after(2000, top.destroy)

    def autenticarPersona(self, code):
        # Verificar si es el profesor
        status = 400
        profesor = self.opening.teacher

        print(code)
        if profesor.qrcode == code:
            titulo = "Autenticación exitosa"
            mensaje = f"Bienvenido, profesor {profesor.full_name()}"
            status = 200
        else:
            estudiante = Student.objects.filter(qrcode=code).first()

            if estudiante:
                matricula = Enrollment.objects.filter(opening=self.opening, student=estudiante).first()
                
                if matricula:
                    titulo = "Autenticación exitosa"
                    mensaje = estudiante.full_name()

                    fecha = datetime.datetime.today().date()

                    asistencia = Attendance()
                    asistencia.enrollment = matricula
                    asistencia.date = fecha
                    asistencia.save()

                    asistencias = Attendance.objects.filter(date=fecha, enrollment=matricula)

                    if asistencias.count() % 2 == 0:
                        mensaje = f"Hasta luego, {mensaje}"
                    else:
                        mensaje = f"Bienvenido, {mensaje}"

                    status = 200
                else:
                    titulo = "Autenticación fallida"
                    mensaje = f"El estudiante no se encuentra inscrito \nen este curso"
            else:
                titulo = "Autenticación fallida"
                mensaje = "El codigo QR proporcionado no esta asociado\na ningun estudiante del curso"

        return status, titulo, mensaje


    def cicloVideo(self):
        esta_cerrado_top = True
        tiempo_top_fue_abierto = None

        while self.terminado == False:
            try:
                self.cuadro = self.camara.read()
                self.cuadro = imutils.resize(self.cuadro, width=340)

                qrcodes = pyzbar.decode(self.cuadro)
                code = None

                for qrcode in qrcodes:
                    (x, y, w, h) = qrcode.rect
                    cv2.rectangle(self.cuadro, (x, y), (x + w, y + h), (246, 209, 81), 1)
                    code = qrcode.data.decode('utf-8')
                    break

                if code and esta_cerrado_top:
                    status, title, message = self.autenticarPersona(code)

                    if status == 200:
                        self.autenticacionExitosa(message=message, title=title)
                    else:
                        self.autenticacionExitosa(message=message, title=title)
                    
                    esta_cerrado_top = False
                    tiempo_top_fue_abierto = time.time()

                if esta_cerrado_top == False:
                    if time.time() - tiempo_top_fue_abierto >= 2:
                        esta_cerrado_top = True

                imagen = cv2.cvtColor(self.cuadro, cv2.COLOR_BGR2RGB)
                imagen = Image.fromarray(imagen)
                imagen = ImageTk.PhotoImage(imagen)

                if self.panelVideo is None:
                    self.panelVideo = tk.Label(self.parent, image=imagen, borderwidth=.5, relief="solid")
                    self.panelVideo.image = imagen
                    self.panelVideo.pack(side="left", padx=60, pady=0)       
                else:
                    self.panelVideo.configure(image=imagen)
                    self.panelVideo.image = imagen
            
            except RuntimeError as e:
                print(f"[INFO] Ha ocurrido un error en tiempo de ejecución: {e}")

            except (KeyboardInterrupt, SystemExit):
                self.terminado = True

            except Exception as e:
                print(f"[INFO] Ha ocurrido un error: {e}")

    def onClose(self):
        print("[INFO] Saliendo de la aplicación")
        self.terminado = True
        self.camara.stop()
        self.parent.quit()


if __name__ == '__main__':
    main = tk.Tk()
    main.title("Sistema asistencia QR")
    main.geometry("1280x720")
    main.config(background="#FFFFFF")

    app = UIMarcajeAsistencia(parent=main)
    app.mainloop()