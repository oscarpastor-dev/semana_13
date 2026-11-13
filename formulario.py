import tkinter as tk
from tkinter import messagebox, ttk
import re
import os

try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

# Ruta de la imagen real del logo de Google.
RUTA_ICONO_GOOGLE = r"D:\Nueva carpeta (3)\images.png"

# Ícono de respaldo (si no se encuentra images.png o no está instalado Pillow)
GOOGLE_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAABT0lEQVR4nMWWMU4DMRBF"
    "/64QDRJdTrA+AA1ItCx1KiRylhwAzkGJxBGI6MkVvCcIUqo0EVIo0KzGw8zYG4H51a49"
    "6+c/HnkHqKxmSnCM8aCNhxCK18kGckjXdWrMMAxHwVXYVFlZIKm7oY8sRzmRY83tj4EY"
    "48EDfa5OAQDXH/NxbH3/YoIl9KRoywyk6fL5zgVzJXTNnQXiDqU4WLpsj4HlRI6B7zrg"
    "hVSc0vGDfg8AWBuAnFprQnNHMCnt7KxNtEC+Mj2YByXxtKoOpbsczIJqLs2U/pWqA9Uq"
    "3T5eJO+zvnzB8+HJnf+flIYQGv6Lmb2+J0Gb26uixfqHXfK+Wp4BSG+bYoc5qIRZMoHS"
    "pQfVYOROaiyaEEJTcgFw6OLmzY0FnMuboN5Zlko7O1L28iZoSeFYaeSa3GJoKZUgr8Vw"
    "Va2JklB6/o02sXojXF1f71sIItI/fx8AAAAASUVORK5CYII="
)


class FormularioRegistro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Usuario")
        self.root.geometry("500x530")

        # Variables de los campos
        self.nombre = tk.StringVar()
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm_pass = tk.StringVar()
        self.edad = tk.StringVar()
        self.genero = tk.StringVar(value="")
        self.acepto = tk.BooleanVar()

        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal con padding
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Título
        tk.Label(
            frame, text="Registro de Usuario",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=(0, 15))

        # Campos de texto: Nombre, Email, Contraseña, Confirmar contraseña
        campos = [
            ("Nombre completo:", self.nombre, False),
            ("Email:", self.email, False),
            ("Contraseña:", self.password, True),
            ("confirmar contraseña:", self.confirm_pass, True),
        ]
        for i, (label, var, oculto) in enumerate(campos):
            fila = i + 1
            tk.Label(frame, text=label, anchor="e").grid(
                row=fila, column=0, sticky="e", pady=5, padx=(0, 10)
            )
            tk.Entry(
                frame, textvariable=var, width=30,
                show="*" if oculto else ""
            ).grid(row=fila, column=1, columnspan=3, pady=5, sticky="w")

        # Fila: Edad + Género (Masculino / Femenino), según el wireframe
        fila_edad_genero = 5
        tk.Label(frame, text="Edad:", anchor="e").grid(
            row=fila_edad_genero, column=0, sticky="e", pady=5
        )
        tk.Entry(frame, textvariable=self.edad, width=6).grid(
            row=fila_edad_genero, column=1, sticky="w", pady=5
        )

        tk.Label(frame, text="Género:").grid(
            row=fila_edad_genero, column=2, sticky="e", padx=(15, 5), pady=5
        )
        genero_frame = tk.Frame(frame)
        genero_frame.grid(row=fila_edad_genero, column=3, sticky="w", pady=5)
        for opcion, letra in [("Masculino", "M"), ("Femenino", "F")]:
            tk.Radiobutton(
                genero_frame, text=letra, variable=self.genero, value=opcion,
                selectcolor="white"
            ).pack(side="left")

        # Fila: Acepto términos (izquierda) + "Otro" (bajo Género, sin
        # desperdiciar espacio), tal como en el wireframe.
        fila_terminos = fila_edad_genero + 1
        tk.Checkbutton(
            frame, text="Acepto términos", variable=self.acepto
        ).grid(row=fila_terminos, column=0, columnspan=2, sticky="w", pady=10)

        tk.Radiobutton(
            frame, text="Otro", variable=self.genero, value="Otro",
            selectcolor="white"
        ).grid(row=fila_terminos, column=3, sticky="w", pady=10)

        # Botones
        fila_botones = fila_terminos + 1
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=fila_botones, column=0, columnspan=4, pady=15)
        self.btn_registrar = tk.Button(
            btn_frame, text="Registrar",
            command=self.validar, width=15,
            bg="#4CAF50", fg="white"
        )
        self.btn_registrar.pack(side="left", padx=10)
        self.btn_limpiar = tk.Button(
            btn_frame, text="Limpiar",
            command=self.limpiar, width=15
        )
        self.btn_limpiar.pack(side="left", padx=10)

        # Botón "continuar con Google", con ícono, según el wireframe
        fila_google = fila_botones + 1
        self.icono_google = self._cargar_icono_google(alto_px=22)
        tk.Button(
            frame, text=" continuar con google",
            image=self.icono_google, compound="left",
            command=self.abrir_login_google, width=180,
            anchor="w", padx=10
        ).grid(row=fila_google, column=0, columnspan=4, pady=(0, 10))

        # Círculo de carga (oculto hasta que se procese el registro)
        self.cargando = ttk.Progressbar(
            frame, mode="indeterminate", length=150
        )
        self.cargando.grid(row=fila_google + 1, column=0, columnspan=4, pady=(0, 10))
        self.cargando.grid_remove()

    def _cargar_icono_google(self, alto_px=22):
        """Carga images.png y la reduce a 'alto_px' de alto, manteniendo
        la proporción. Si no existe el archivo o no hay Pillow instalado,
        usa el ícono de respaldo incrustado en el código."""
        if PIL_DISPONIBLE and os.path.exists(RUTA_ICONO_GOOGLE):
            try:
                imagen = Image.open(RUTA_ICONO_GOOGLE)
                proporcion = alto_px / imagen.height
                nuevo_ancho = max(1, int(imagen.width * proporcion))
                imagen = imagen.resize((nuevo_ancho, alto_px), Image.LANCZOS)
                return ImageTk.PhotoImage(imagen)
            except Exception:
                pass
        # Respaldo: ícono simplificado incrustado en base64
        return tk.PhotoImage(data=GOOGLE_ICON_B64)

    def abrir_login_google(self):
        # Ventana secundaria que simula el inicio de sesión con Google,
        # según el segundo recuadro del wireframe.
        ventana_google = tk.Toplevel(self.root)
        ventana_google.title("Iniciar sesión con Google")
        ventana_google.geometry("350x180")
        ventana_google.resizable(False, False)
        ventana_google.transient(self.root)
        ventana_google.grab_set()  # bloquea la ventana principal mientras está abierta

        contenedor = tk.Frame(ventana_google, padx=20, pady=20)
        contenedor.pack(fill="both", expand=True)

        tk.Label(contenedor, text="ingresa correo").grid(row=0, column=0, sticky="e", pady=10)
        usuario_var = tk.StringVar()
        tk.Entry(contenedor, textvariable=usuario_var, width=15).grid(row=0, column=1)
        tk.Label(contenedor, text="@gmail.com").grid(row=0, column=2, sticky="w", padx=(5, 0))

        def ingresar():
            usuario = usuario_var.get().strip()
            if not usuario:
                messagebox.showerror("Error", "Ingresa un correo válido", parent=ventana_google)
                return
            # Autocompleta el formulario con los datos de la cuenta de Google
            self.email.set(f"{usuario}@gmail.com")
            if not self.nombre.get().strip():
                self.nombre.set(usuario.replace(".", " ").title())
            ventana_google.destroy()
            messagebox.showinfo(
                "Sesión iniciada",
                f"Sesión iniciada con {usuario}@gmail.com"
            )

        tk.Button(
            contenedor, text="ingresar", command=ingresar, width=15
        ).grid(row=1, column=0, columnspan=3, pady=15)

        usuario_var.set("")
        contenedor.winfo_children()[1].focus_set()

    def validar(self):
        errores = []

        # Nombre obligatorio
        if not self.nombre.get().strip():
            errores.append("El nombre es obligatorio")

        # Email con formato válido
        email = self.email.get().strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errores.append("Email inválido (debe contener @ y dominio)")

        # Contraseña mínimo 8 caracteres
        if len(self.password.get()) < 8:
            errores.append("La contraseña debe tener mínimo 8 caracteres")

        # Contraseñas coinciden
        if self.password.get() != self.confirm_pass.get():
            errores.append("Las contraseñas no coinciden")

        # Edad válida
        try:
            edad = int(self.edad.get())
            if edad < 15 or edad > 99:
                errores.append("La edad debe estar entre 15 y 99")
        except ValueError:
            errores.append("La edad debe ser un número")

        # Género seleccionado
        if not self.genero.get():
            errores.append("Seleccione un género")

        # Términos aceptados
        if not self.acepto.get():
            errores.append("Debe aceptar los términos")

        if errores:
            messagebox.showerror(
                "Errores de validación",
                "\n".join(f"• {e}" for e in errores)
            )
            return

        # Datos válidos: mostrar el círculo de carga antes de confirmar
        self.btn_registrar.config(state="disabled")
        self.btn_limpiar.config(state="disabled")
        self.cargando.grid()
        self.cargando.start(10)
        self.root.after(1200, self._finalizar_registro)

    def _finalizar_registro(self):
        self.cargando.stop()
        self.cargando.grid_remove()
        self.btn_registrar.config(state="normal")
        self.btn_limpiar.config(state="normal")
        messagebox.showinfo(
            "Registro exitoso",
            f"¡Bienvenido {self.nombre.get()}!\n"
            f"Email: {self.email.get()}"
        )

    def limpiar(self):
        for var in [self.nombre, self.email, self.password,
                    self.confirm_pass, self.edad, self.genero]:
            var.set("")
        self.acepto.set(False)


if __name__ == "__main__":
    app = FormularioRegistro()
    app.root.mainloop()