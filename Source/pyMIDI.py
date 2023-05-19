import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

def process_midi_file(input_file, output_file):
    try:
        # Código para processar o arquivo MIDI
        # ...
        # Exemplo de salvamento do arquivo de saída
        shutil.copyfile(input_file, output_file)
        messagebox.showinfo("Concluído", "Processamento do arquivo MIDI concluído com sucesso!")
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo MIDI selecionado não foi encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo MIDI: {str(e)}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos MIDI", "*.mid")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(tk.END, file_path)

def process_file():
    input_file = entry_file.get()
    if not input_file:
        messagebox.showwarning("Aviso", "Selecione um arquivo MIDI antes de processar.")
        return

    output_file = os.path.splitext(input_file)[0] + "_processed.mid"
    if os.path.exists(output_file):
        result = messagebox.askyesno("Arquivo Existente", "O arquivo de saída já existe. Deseja substituí-lo?")
        if not result:
            return

    process_midi_file(input_file, output_file)

# Criar a janela principal
window = tk.Tk()
window.title("Processamento de Arquivo MIDI")

# Configurar imagem de fundo
background_image = tk.PhotoImage(file="background.png")
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Criar os componentes da interface
label_file = tk.Label(window, text="Arquivo MIDI:", bg="white")
label_file.pack()

entry_file = tk.Entry(window, width=50)
entry_file.pack()

button_select = tk.Button(window, text="Selecionar", command=select_file)
button_select.pack()

button_process = tk.Button(window, text="Processar", command=process_file)
button_process.pack()

# Iniciar o loop de eventos da interface gráfica
window.mainloop()
