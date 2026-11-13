import tkinter as tk
from tkinter import messagebox
import re


class FormularioRegistro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Usuario")
        self.root.geometry("400x350")

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
            font=("Arial", 20, "bold")
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
                genero_frame, text=letra, variable=self.genero, value=opcion
            ).pack(side="left")

        # Fila: Acepto términos (izquierda) + "Otro" (bajo Género, sin
        # desperdiciar espacio), tal como en el wireframe.
        fila_terminos = fila_edad_genero + 1
        tk.Checkbutton(
            frame, text="Acepto términos", variable=self.acepto
        ).grid(row=fila_terminos, column=0, columnspan=1, sticky="w", pady=10)

        tk.Radiobutton(
            frame, text="Otro", variable=self.genero, value="Otro"
        ).grid(row=fila_terminos, column=3, sticky="w", pady=10)

        # Botones
        fila_botones = fila_terminos + 1
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=fila_botones, column=0, columnspan=4, pady=15)
        tk.Button(
            btn_frame, text="Registrar",
            command=self.validar, width=15,
            bg="#0BF213", fg="white"
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame, text="Limpiar",
            command=self.limpiar, width=15,
            bg="#0B25E6", fg="white"
        ).pack(side="left", padx=10)

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
        else:
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
