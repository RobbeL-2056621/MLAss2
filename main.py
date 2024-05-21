import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from joblib import load
from keras import saving, layers
from skimage.transform import resize
import skimage as ski
import numpy as np
categories = ["CombWrench", "Hammer", "Screwdriver", "Wrench"]
class ImageClassifier:
    def __init__(self, master):
        self.master = master
        master.title("Image Processor")

        self.image = None
        self.model = None

        self.label = tk.Label(master, text="Authors:\n Robbe Lenaerts \nRobin Weynjes", font=("Helvetica", 10))
        self.label.pack()

        self.load_image_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_image_button.pack()

        self.load_model_button = tk.Button(master, text="Load Model", command=self.load_model)
        self.load_model_button.pack()

        self.compute_button = tk.Button(master, text="Compute", command=self.compute, state=tk.DISABLED)
        self.compute_button.pack()

        self.result_label = tk.Label(master, text="Result: ")
        self.result_label.pack()

        self.master.update()
        min_width = max(200, self.master.winfo_width())
        self.master.minsize(min_width, self.master.winfo_height())


    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.JPEG")])
        if file_path:
            self.image = ski.io.imread(file_path)
            self.load_image_button.config(text="Change Image")
            self.check_compute_button()

    def load_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("ML model", "*.keras")])
        if file_path:
            self.model = saving.load_model(file_path)
            self.load_model_button.config(text="Change Model")
            self.check_compute_button()

    def compute(self):
        #TODO
        if self.image is not None and self.model is not None:
            results = self.model.predict(np.asarray([resize(self.image, (300, 300))]))
            softmax_layer = layers.Softmax()
            probabilities = np.array(softmax_layer(results))[0]
            index = np.argmax(probabilities)
            prediction = categories[index]
            prob = probabilities[index]
            self.result_label.config(text=f"Predicted to be {prediction} with probability {prob}.")

    def check_compute_button(self):
        if self.image is not None and self.model is not None:
            self.compute_button.config(state=tk.NORMAL)
        else:
            self.compute_button.config(state=tk.DISABLED)


root = tk.Tk()
app = ImageClassifier(root)
root.mainloop()
