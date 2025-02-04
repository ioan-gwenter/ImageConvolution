"""
ui.py

Contains the Tkinter-based UI for displaying images and allowing user interactions.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from PIL import Image, ImageTk

from image_processor import Kernel, ImageProcessor


class MainApplication(tk.Tk):
    """
    Main Tkinter Application.
    """
    def __init__(self) -> None:
        super().__init__()
        
        self.title("Cwk 1 Image Processor")
        # self.geometry("1500x1200")
        
        self.image_processor = ImageProcessor();

        # Kernel config

        self.selected_kernel = None

        # Create a StringVar to store the input image path
        self.image_path_var = tk.StringVar(value="")

        # --- Initialize UI Elements ---
        # 1) Top-level frames: we want top left for images, top right for options, bottom for save
        self._create_main_frames()

        # 2) Top Frame: Display and lets user select image file path
        self._create_top_panel()

        # 3) Inside left frame: kernel image display (top), thresholding image display (bottom)
        self._create_image_panes()

        # 4) Inside right frame: kernel options (top), thresholding options (bottom)
        self._create_options_panes()

        # 5) Bottom frame: path selection + "Save" button
        self._create_bottom_panel()



    def _create_main_frames(self) -> None:
        """
        Creates the main horizontal sections:
          1) Left Frame for images
          2) Right Frame for options
          3) Bottom Frame for file save
        """
        # Top container (images + options)
        self.top_container = tk.Frame(self)
        self.top_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

         # Bottom frame: for saving
        self.top_frame = tk.Frame(self.top_container, bg="lightblue", height=50,  pady=5)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH)

        # Left frame: for image panes
        self.image_frame = tk.Frame(self.top_container, bg="lightgray")
        self.image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Right frame: for options
        self.options_frame = tk.Frame(self.top_container, bg="blue")
        self.options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bottom frame: for saving
        self.bottom_frame = tk.Frame(self.top_container, bg="lightblue", height=50, pady=10)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def _create_image_panes(self) -> None:
        """
        Create the two vertical sections in the left frame:
         - Top: kernel result image
         - Bottom: threshold result image
        """
        # split the image_frame vertically
        self.kernel_image_frame = tk.Frame(self.image_frame, bg="white", height=500)
        self.kernel_image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.threshold_image_frame = tk.Frame(self.image_frame, bg="white", height=500)
        self.threshold_image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Inside each frame, place a label or canvas to show the image
        self.kernel_image_label = tk.Label(self.kernel_image_frame, text="Kernel Image Preview")
        self.kernel_image_label.pack(pady=10)

        self.threshold_image_label = tk.Label(self.threshold_image_frame, text="Threshold Image Preview")
        self.threshold_image_label.pack(pady=10)

    def _create_options_panes(self) -> None:
        """
        Create the two vertical sections in the right frame:
         - Top: kernel options
         - Bottom: thresholding options
        """
        self.kernel_options_frame = tk.Frame(self.options_frame, bg="lightyellow", height=50)
        self.kernel_options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.threshold_options_frame = tk.Frame(self.options_frame, bg="lightgreen", height=50)
        self.threshold_options_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Kernel Options ---
        kernel_label = tk.Label(self.kernel_options_frame, text="Kernel Options", bg="lightyellow")
        kernel_label.pack(pady=5)

        self.kernel_var = tk.StringVar()
        self.kernel_dropdown = ttk.Combobox(self.kernel_options_frame, textvariable=self.kernel_var, values=self.image_processor.available_kernels)
        self.kernel_dropdown.set("Select kernel")
        self.kernel_dropdown.pack(side=tk.TOP, pady=5)
        self.kernel_dropdown.bind("<<ComboboxSelected>>", self.on_kernel_selected)

        self.kernel_options_content_frame = tk.Frame(self.kernel_options_frame, bg="red")
        self.kernel_options_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.apply_kernel_button = tk.Button(self.kernel_options_frame, text="Apply Kernel", command=self.on_apply_kernel)
        self.apply_kernel_button.pack(side=tk.TOP)

        # --- Thresholding Options ---
        threshold_label = tk.Label(self.threshold_options_frame, text="Threshold Options", bg="lightgreen")
        threshold_label.pack(pady=5)

        self.threshold_value_var = tk.StringVar(value="128")
        threshold_entry = tk.Entry(self.threshold_options_frame, textvariable=self.threshold_value_var)
        threshold_entry.pack(pady=5)

        self.auto_threshold_var = tk.BooleanVar(value=False)
        auto_check = tk.Checkbutton(self.threshold_options_frame, text="Use Automatic", variable=self.auto_threshold_var)
        auto_check.pack(pady=5)

        self.apply_threshold_button = tk.Button(self.threshold_options_frame, text="Apply Threshold", command=self.on_apply_threshold)
        self.apply_threshold_button.pack(pady=5)

    def _create_bottom_panel(self) -> None:
        """
        Creates the bottom panel for selecting file path and saving.
        """
        tk.Label(self.bottom_frame, text="Save Path:", bg="lightblue").pack(side=tk.LEFT, padx=5)
    
        self.save_path_var = tk.StringVar()
        self.save_path_entry = tk.Entry(self.bottom_frame, textvariable=self.save_path_var, width=50)
        self.save_path_entry.pack(side=tk.LEFT, padx=5)

        browse_button = tk.Button(self.bottom_frame, text="Browse...", command=self.on_browse_dir)
        browse_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(self.bottom_frame, text="Save Image", command=self.on_save_image)
        save_button.pack(side=tk.LEFT, padx=5)

    def _create_top_panel(self) -> None:
        """
        Creates a top panel for selecting the target/input image to process.
        """

        # Label
        self.top_text_entry_frame = tk.Frame(self.top_frame, bg="lightblue")
        tk.Label(self.top_text_entry_frame, text="Select Image:", bg="lightblue").pack(side=tk.LEFT, padx=5)
        # Entry to display telf.text_entry_frame = he chosen file path
        self.image_path_entry = tk.Entry(self.top_text_entry_frame, textvariable=self.image_path_var, width=50)
        self.image_path_entry.pack(side=tk.LEFT, padx=5)

        # Browse button
        browse_button = tk.Button(self.top_text_entry_frame, text="Browse...", command=self.on_browse_input_image)
        browse_button.pack(side=tk.LEFT, padx=5)

         # Image Preview Label (Fixed Size)
        image = Image.open('./default.png')  # Open image
        image.thumbnail((50, 50))
        place_holder= ImageTk.PhotoImage(image)
        self.image_preview_label = tk.Label(self.top_text_entry_frame, bg="gray", width=50, height=50,image=place_holder)  # Placeholder
        self.image_preview_label.pack(side=tk.LEFT, padx=25)

        self.top_text_entry_frame.pack(side=tk.TOP)

    def _create_bottom_panel(self) -> None:
        """
        Creates the bottom panel for selecting file path and saving.
        """
        self.bottom_text_entry_frame = tk.Frame(self.bottom_frame, bg="lightblue")

        tk.Label(self.bottom_text_entry_frame, text="Save Path:", bg="lightblue").pack(side=tk.LEFT, padx=5)

        self.save_path_var = tk.StringVar()
        self.save_path_entry = tk.Entry(self.bottom_text_entry_frame, textvariable=self.save_path_var, width=50)
        self.save_path_entry.pack(side=tk.LEFT, padx=5)

        browse_button = tk.Button(self.bottom_text_entry_frame, text="Browse...", command=self.on_browse_dir)
        browse_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(self.bottom_text_entry_frame, text="Save Image", command=self.on_save_image)
        save_button.pack(side=tk.LEFT, padx=5)

        self.bottom_text_entry_frame.pack(side=tk.TOP)

    def _update_image_preview(self, file_path: str) -> None:
        """
        Updates the image preview label with a resized version of the selected image.
        :param file_path: Path to the image file.
        """
        try:
            image = Image.open(file_path)  # Open image
            image.thumbnail((50, 50))  # Resize while maintaining aspect ratio

            # Convert to Tkinter image format
            self.tk_image = ImageTk.PhotoImage(image)

            # Set image in label
            self.image_preview_label.config(image=self.tk_image)
            self.image_preview_label.image = self.tk_image  # Keep reference to avoid garbage collection

        except Exception as e:
            print(f"Error loading preview: {e}")

    # ---------------------------
    #       EVENT HANDLERS
    # ---------------------------

    def on_kernel_selected(self, event=None) -> None:
        """
        Called when the user selects a kernel from the dropdown.
        """
        selected_name = self.kernel_var.get()
        for k in self.image_processor.available_kernels:
            if k == selected_name:
                self.selected_kernel = k
                break

    def on_apply_kernel(self) -> None:
        """
        Applies the selected kernel to the original image data.
        """
        if not self.selected_kernel:
            messagebox.showwarning("No Kernel Selected", "Please select a kernel first.")
            return

        # Apply kernel
        # self.kernel_image_data = apply_kernel(self.original_image_data, self.selected_kernel)
        # Update UI (placeholder text)
        self.kernel_image_label.config(text=f"Kernel: {self.selected_kernel} applied")

    def on_apply_threshold(self) -> None:
        """
        Applies thresholding to the kernel image data (or original).
        """
        try:
            threshold_val = int(self.threshold_value_var.get())
        except ValueError:
            messagebox.showwarning("Invalid Value", "Threshold value must be an integer.")
            return

        use_auto = self.auto_threshold_var.get()
        # Apply threshold
        # self.threshold_image_data = apply_threshold(self.kernel_image_data, threshold_val, use_auto=use_auto)
        self.threshold_image_label.config(text=f"Threshold applied (val={threshold_val}, auto={use_auto})")

    def on_browse_dir(self) -> None:
        """
        Prompt user to select a directory where processed images will be saved.
        """
        directory = filedialog.askdirectory(
            title="Choose Save Directory"
        )
        if directory:  # Ensure user didn't cancel
            self.save_path_var.set(directory)


    def on_browse_input_image(self) -> None:
        """
        Opens a file dialog for the user to select an image file.
        """
        filename = filedialog.askopenfilename(
            title="Choose an image file",
            filetypes=[("Image Files", "*.*"), ("All Files", "*.*")]
        )
        if filename:
            self.image_path_var.set(filename)  # Update entry field
            self._update_image_preview(filename)  # Load preview
                

    def on_save_image(self) -> None:
        """
        Save the processed image to the specified path (placeholder).
        """
        save_path = self.save_path_var.get()
        if not save_path:
            messagebox.showwarning("No Path", "Please specify a path to save the image.")
            return

        if ImageProcessor.save_results(self, dir_path=save_path):
            messagebox.showinfo("Save Image", f"Image saved (pretend) to: {save_path}")
        else:
            messagebox.showerror("Error", "Error When Saving Results. Check File Path.")
        return

            
