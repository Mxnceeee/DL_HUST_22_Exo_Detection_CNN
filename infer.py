import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from io import BytesIO
from PIL import Image, ImageTk

# if infer.py doesn't work, copy the full path
model = load_model('cnn_model.keras') 
data = pd.read_csv('exoTrain.csv')


def plot_light_curve(star_index):
    star_data = data.iloc[star_index, 1:].values
    plt.figure(figsize=(12, 4))
    plt.plot(range(len(star_data)), star_data)
    plt.xlabel('Time')
    plt.ylabel('Flux')
    plt.title(f'Light Curve for Star {star_index}')
    

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()  
    return buffer


def predict_star():
    try:
        star_index = int(entry_star_index.get())
        if star_index < 0 or star_index >= len(data):
            raise ValueError("Index out of limites.")
        
        # Prédiction
        star_data = data.iloc[star_index, 1:].values.reshape(1, -1)
        prediction = (model.predict(star_data) > 0.5).astype(int)[0][0]
        result = "Exoplanet Detected" if prediction == 1 else "No Exoplanet Detected"

        
        lbl_result.config(text=f"Prediction: {result}", fg="green")

        
        buffer = plot_light_curve(star_index)
        img = Image.open(buffer)
        img_tk = ImageTk.PhotoImage(img)
        lbl_image.config(image=img_tk)
        lbl_image.image = img_tk  
        buffer.close() 

    except ValueError as e:
        messagebox.showerror("Error", f"Wrong Input : {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error : {e}")

# Interface Tkinter
root = tk.Tk()
root.title("Exoplanet Detection")

# Widgets
frame = tk.Frame(root)
frame.pack(pady=10)

lbl_instruction = tk.Label(frame, text="Enter the index of a star (0 to N):")
lbl_instruction.grid(row=0, column=0, padx=5, pady=5)

entry_star_index = tk.Entry(frame, width=10)
entry_star_index.grid(row=0, column=1, padx=5, pady=5)

btn_predict = tk.Button(frame, text="Predict", command=predict_star)
btn_predict.grid(row=0, column=2, padx=5, pady=5)

lbl_result = tk.Label(root, text="", font=("Arial", 14))
lbl_result.pack(pady=10)

lbl_image = tk.Label(root)
lbl_image.pack(pady=10)


root.mainloop()
