import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import cv2
import os
import numpy as np
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image
OUTPUT_WIDTH = 640 ## Final height of window shown
OUTPUT_HEIGHT = 480 ## Final width of window shown 

# Load MediaPipe Segmentation model
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation_model = mp_selfie_segmentation.SelfieSegmentation(model_selection=0) # model-selection= 1 can also be used

def replace_background(image, background_image):
    """Replaces the background of an input image with a new background image."""
    background_image = cv2.resize(background_image, (image.shape[1], image.shape[0]))
    results = segmentation_model.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.8 ## 0.8 is foreground Thresh which can be adjusted
    output_image = np.where(condition, image, background_image)
    return output_image

def load_background_images(folder_path):
    """Load all background images from the specified folder."""
    background_images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            if image is not None:
                background_images.append(image)
            else:
                print(f"Warning: Could not load image {filename}")
    return background_images

def save_output_image(output_image):
    """Save the output image to a file."""
    save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if save_path:
        cv2.imwrite(save_path, output_image)
        messagebox.showinfo("Success", f"Image saved to {save_path}")

def process_single_image(image_path, background_folder_path):
    """Process a single input image and replace the background."""
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

    image_resized = cv2.resize(image, (OUTPUT_WIDTH, OUTPUT_HEIGHT))

    background_images = load_background_images(background_folder_path)
    if not background_images:
        messagebox.showerror("Error", "No background images found in the folder.")
        return

    background_index = 0
    while True:
        background_image = background_images[background_index % len(background_images)]
        output_image = replace_background(image_resized, background_image)

        cv2.imshow("Image Viewer - Press 'n' for next, 'p' for previous, 's' to save, 'q' to quit", output_image)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('n'):
            background_index = (background_index + 1) % len(background_images)
        elif key == ord('p'):
            background_index = (background_index - 1) % len(background_images)
        elif key == ord('s'):
            save_output_image(output_image)
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

def process_video(video_path, background_folder_path, record_output=False):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open the video file.")
        return

    background_images = load_background_images(background_folder_path)
    if not background_images:
        messagebox.showerror("Error", "No background images found in the folder.")
        return

    if record_output:
        save_path = filedialog.asksaveasfilename(defaultextension='.avi', filetypes=[("AVI files", "*.avi"), ("MP4 files", "*.mp4")])
        if not save_path:
            messagebox.showerror("Error", "No save path specified for video recording.")
            return

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(save_path, fourcc, 20.0, (OUTPUT_WIDTH, OUTPUT_HEIGHT))

    background_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_resized = cv2.resize(frame, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
        background_image = background_images[background_index % len(background_images)]
        output_frame = replace_background(frame_resized, background_image)

        if record_output:
            out.write(output_frame)

        cv2.imshow("Video Viewer - Press 'n' for next, 'p' for previous, 's' to save, 'q' to quit", output_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('n'):
            background_index = (background_index + 1) % len(background_images)
        elif key == ord('p'):
            background_index = (background_index - 1) % len(background_images)
        elif key == ord('s'):
            save_output_image(output_frame)
        elif key == ord('q'):
            break

    cap.release()
    if record_output:
        out.release()
    cv2.destroyAllWindows()

def process_webcam(background_folder_path, record_output=False):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    if record_output:
        save_path = filedialog.asksaveasfilename(defaultextension='.avi', filetypes=[("AVI files", "*.avi"), ("MP4 files", "*.mp4")])
        if save_path:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(save_path, fourcc, 20.0, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
        else:
            messagebox.showerror("Error", "Could not set save path for recording.")
            return

    background_images = load_background_images(background_folder_path)
    if not background_images:
        messagebox.showerror("Error", "No background images found in the folder.")
        return

    background_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_resized = cv2.resize(frame, (OUTPUT_WIDTH, OUTPUT_HEIGHT))
        background_image = background_images[background_index % len(background_images)]
        output_frame = replace_background(frame_resized, background_image)

        if record_output and save_path:
            out.write(output_frame)

        cv2.putText(output_frame, f"FPS: {int(cap.get(cv2.CAP_PROP_FPS))}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("Webcam - Press 'n' for next, 'p' for previous, 'q' to quit", output_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('n'):
            background_index = (background_index + 1) % len(background_images)
        elif key == ord('p'):
            background_index = (background_index - 1) % len(background_images)
        elif key == ord('q'):
            break

    cap.release()
    if record_output:
        out.release()
    cv2.destroyAllWindows()

def open_file_dialog(mode):
    """Open file dialog to select image/video."""
    if mode == 'image':
        return filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    elif mode == 'video':
        return filedialog.askopenfilename(title="Select a Video", filetypes=[("Video files", "*.mp4;*.avi;*.mov")])

def open_background_folder_dialog():
    """Open folder dialog to select background images."""
    return filedialog.askdirectory(title="Select Background Folder")

def start_gui():
    """Start the GUI application."""
    root = tk.Tk()
    root.title("Background Replacer")

    def on_start_button_click():
        mode = mode_var.get()
        if mode not in ['image', 'video', 'webcam']:
            messagebox.showerror("Error", "Please select a valid mode.")
            return
        record_option = record_var.get()
        background_folder = open_background_folder_dialog()
        if not background_folder:
            messagebox.showerror("Error", "No background folder selected.")
            return

        if mode == 'image':
            image_path = open_file_dialog('image')
            if image_path:
                process_single_image(image_path, background_folder)
        elif mode == 'video':
            video_path = open_file_dialog('video')
            if video_path:
                process_video(video_path, background_folder, record_output=record_option)
        elif mode == 'webcam':
            process_webcam(background_folder, record_output=record_option)

    mode_var = tk.StringVar(value='image')
    tk.Label(root, text="Select Mode").pack()
    tk.Radiobutton(root, text="Image", variable=mode_var, value='image').pack()
    tk.Radiobutton(root, text="Video", variable=mode_var, value='video').pack()
    tk.Radiobutton(root, text="Webcam", variable=mode_var, value='webcam').pack()


    # Checkbox to record output for webcam
    record_var = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="Save Video Output", variable=record_var).pack()
    tk.Button(root, text="Start", command=on_start_button_click).pack()

    root.mainloop()
 

if __name__ == "__main__":
    start_gui()