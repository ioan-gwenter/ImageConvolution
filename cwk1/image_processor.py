import numpy as np
from typing import List, Optional, Tuple
import cv2 

class ImageProcessor:
    """
    Class for kernel-based convolution and thresholding.
    """

    def __init__(self) -> None:
        """
        Initialize ImageProcessor with a given image file.
        :param image_path: Path to the image file to be processed.
        """
        self.input_image_path = None
        self.input_image_data = None

        self.available_kernels = ["Gaussian", "Average", "Custom"]
        self.current_kernel = None

    # ---------------------------
    #       KERNEL MANAGER
    # ---------------------------

    def get_available_kernels(self) -> List:
        return self.available_kernels

    def get_current_kernel(self) -> List:
        return self.current_kernel
    
    def update_kernel(self, kernel_type: str, **params) -> None:
        """
        Updates the current kernel based on the selected type and parameters.
        
        :param kernel_type: The type of kernel .
        :param params: Additional parameters required for the kernel.
        """
        if kernel_type == "Gaussian":
            size = params.get("size")
            sigma = params.get("sigma")
            self.current_kernel = self._generate_gaussian_kernel(size, sigma)
        elif kernel_type == "Average":
            size = params.get("size")
            self.current_kernel = self._generate_average_kernel(size)
        else:
            self.current_kernel = None
            raise ValueError(f"Unsupported kernel type: {kernel_type}")

    def _generate_gaussian_kernel(self, size: int, sigma: float) -> np.ndarray:
        """
        Generates a 2D Gaussian kernel.

        :param size: The size of the kernel (size x size).
        :param sigma: The standard deviation of the Gaussian distribution.
        :return: A 2D NumPy array representing the Gaussian kernel.
        """
        if size % 2 == 0:
            raise ValueError("Kernel size must be odd to ensure a center pixel.")

        # Define the kernel grid (centered at 0)
        k = size // 2
        x, y = np.meshgrid(np.arange(-k, k + 1), np.arange(-k, k + 1))

        # Compute the Gaussian function
        gaussian_kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        
        # Normalize the kernel so that the sum equals 1
        gaussian_kernel /= np.sum(gaussian_kernel)

        return gaussian_kernel
    
    def _generate_average_kernel(self, size: int) -> np.ndarray:
        """
        Generates an averaging kernel of given size.

        :param size: The size of the kernel (size x size).
        :return: A 2D NumPy array representing the averaging kernel.
        """
        if size % 2 == 0:
            raise ValueError("Kernel size must be an odd integer to ensure a center pixel.")

        # Create an NxN matrix filled with 1s
        kernel = np.ones((size, size), dtype=np.float32)

        # Normalize by dividing each element by the total number of elements
        kernel /= (size * size)

        return kernel
        

    def apply_kernel(self) -> np.ndarray:
        """
        Applies a convolutional kernel to the image.
        :param kernel: Kernel object containing name and matrix.
        :return: Processed 2D NumPy array.
        """
        return False

    # ---------------------------
    #       IMAGE MANAGER
    # ---------------------------

    def set_target_image(self, file_path: str) -> bool:
        """
        Sets the image path and loads the image in grayscale.
        
        :param file_path: Path to the image file.
        :return: True if the image is successfully loaded, False otherwise.
        """
        try:
            self.input_image_data = self.load_image_grayscale(file_path=file_path)
            self.input_image_path = file_path 
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
        
    def save_results(self, dir_path:str = '/') -> bool:
        try:
            # self._save_image(dir_path) TODO
            return True
        except Exception as e:
            print(f"Error saving results: {e}")
            return False
        
    def _save_image(self, output_path: str, image_array: np.ndarray) -> None:
        """
        Saves an image to the specified file path.
        :param output_path: File path to save the image.
        :param image_array: 2D NumPy array to save.
        """
        return cv2.imwrite(output_path, image_array)

    def load_image_grayscale(self, file_path: str) -> np.ndarray:
        """
        Loads an image as a 2D NumPy array in grayscale.
        :param file_path: Path to the image file.
        :return: 2D NumPy array representing pixel intensities (0-255).
        """
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Failed to load image: {file_path}")
        return image

    
