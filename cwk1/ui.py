"""
ui.py

Contains the Tkinter-based UI for displaying images and allowing user interactions.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from PIL import Image, ImageTk
import numpy as np

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

    def _build_kernel_options(self) -> None:
        """
        Builds and updates the kernel options panel based on the selected kernel type.
        """
        # Clear previous options
        for widget in self.kernel_options_content_frame.winfo_children():
            widget.destroy()

        # Left-side options panel
        options_panel = tk.Frame(self.kernel_options_content_frame, bg="lightyellow")
        options_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Right-side kernel preview panel
        self.kernel_preview_canvas = tk.Canvas(self.kernel_options_content_frame, width=100, height=100, bg="white")
        self.kernel_preview_canvas.pack(side=tk.RIGHT, padx=10, pady=10)

        # Add kernel size input (common for all kernels)
        tk.Label(options_panel, text="Kernel Size N:").pack(pady=2)
        self.kernel_size_var = tk.IntVar(value=3)
        tk.Entry(options_panel, textvariable=self.kernel_size_var, width=5).pack(pady=2)

        # Bind event to update kernel preview
        self.kernel_size_var.trace_add("write", self._on_kernel_param_change)

        # Additional options for specific kernels
        if self.selected_kernel == "Gaussian":
            tk.Label(options_panel, text="Sigma:").pack(pady=2)
            self.sigma_var = tk.DoubleVar(value=1.0)
            tk.Entry(options_panel, textvariable=self.sigma_var, width=5).pack(pady=2)
            self.sigma_var.trace_add("write", self._on_kernel_param_change)

        elif self.selected_kernel == "Sobel":
            tk.Label(options_panel, text="Edge Direction:").pack(pady=2)
            self.edge_dir_var = tk.StringVar(value="Horizontal")
            ttk.Combobox(options_panel, textvariable=self.edge_dir_var, values=["Horizontal", "Vertical"]).pack(pady=2)
            self.edge_dir_var.trace_add("write", self._on_kernel_param_change)

        elif self.selected_kernel == "Laplacian":
            tk.Label(options_panel, text="Scale Factor:").pack(pady=2)
            self.scale_var = tk.DoubleVar(value=1.0)
            tk.Entry(options_panel, textvariable=self.scale_var, width=5).pack(pady=2)
            self.scale_var.trace_add("write", self._on_kernel_param_change)

        # Refresh UI
        self.kernel_options_content_frame.update_idletasks()
        self._update_kernel_preview()


    # ---------------------------
    #       EVENT HANDLERS
    # ---------------------------

    def on_kernel_selected(self, event=None) -> None:
        """
        Called when the user selects a kernel from the dropdown.
        """
        selected_name = self.kernel_var.get()
        if selected_name in self.image_processor.available_kernels:
            self.selected_kernel = selected_name
            self._build_kernel_options()  # Refresh the UI with relevant fields

    def _on_kernel_param_change(self, *args) -> None:
        """
        Called whenever a kernel-related input field is modified.
        It updates the kernel and refreshes the preview.
        """
        # Gather current kernel settings
        kernel_size = self.kernel_size_var.get()
        params = {"size": kernel_size}

        if self.selected_kernel == "Gaussian":
            params["sigma"] = self.sigma_var.get()
        elif self.selected_kernel == "Sobel":
            params["direction"] = self.edge_dir_var.get()
        elif self.selected_kernel == "Laplacian":
            params["scale"] = self.scale_var.get()

        # Update the kernel in the ImageProcessor
        self.image_processor.update_kernel(self.selected_kernel, **params)

        # Refresh the preview
        self._update_kernel_preview()

    def _update_kernel_preview(self) -> None:
        """
        Retrieves the kernel matrix from the ImageProcessor, converts it into an image,
        and displays it in the kernel preview canvas.
        """
        if not self.selected_kernel:
            return

        # Get the kernel matrix (2D list) from the ImageProcessor
        kernel_matrix = self.image_processor.get_kernel()

        if not kernel_matrix:
            return

        kernel_array = np.array(kernel_matrix)

        # Normalize values for better visualization
        kernel_min, kernel_max = kernel_array.min(), kernel_array.max()
        if kernel_max > kernel_min:  # Avoid division by zero
            kernel_array = (kernel_array - kernel_min) / (kernel_max - kernel_min) * 255

        
        kernel_image = Image.fromarray(kernel_array.astype("uint8"))
        kernel_image = kernel_image.resize((100, 100), Image.NEAREST)

        # Convert to Tkinter-compatible image
        self.kernel_preview_image = ImageTk.PhotoImage(kernel_image)

        # Display in the canvas
        self.kernel_preview_canvas.create_image(50, 50, image=self.kernel_preview_image)
        self.kernel_preview_canvas.image = self.kernel_preview_image  # Prevent garbage collection


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

            
