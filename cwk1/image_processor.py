import numpy as np
from typing import List, Optional, Tuple
from dataclasses import dataclass
import cv2 

@dataclass
class Kernel:
    """
    Represents a convolution kernel.
    """
    name: str
    matrix: np.ndarray

class ImageProcessor:
    """
    Class for performing image processing operations such as
    kernel-based convolution and thresholding.
    """

    def __init__(self) -> None:
        """
        Initialize ImageProcessor with a given image file.
        :param image_path: Path to the image file to be processed.
        """
        self.input_image_path = None
        self.input_image_data = None

        self.available_kernels = ["Gaussian", "Average", "Custom"]

    def get_available_kernels(self) -> List:
        return self.available_kernels

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

    def apply_kernel(self, kernel: Kernel) -> np.ndarray:
        """
        Applies a convolutional kernel to the image.
        :param kernel: Kernel object containing name and matrix.
        :return: Processed 2D NumPy array.
        """
        kernel_size = kernel.matrix.shape[0]
        pad_size = kernel_size // 2  # Padding size

        # Pad image with zeros to maintain dimensions after convolution
        padded_image = np.pad(self.image_data, pad_size, mode='constant', constant_values=0)

        # Prepare an empty output image
        output = np.zeros_like(self.image_data, dtype=np.float32)

        # Convolution operation
        for i in range(self.image_data.shape[0]):  # Loop over height
            for j in range(self.image_data.shape[1]):  # Loop over width
                region = padded_image[i:i + kernel_size, j:j + kernel_size]
                output[i, j] = np.sum(region * kernel.matrix)

        # Normalize and convert back to 8-bit
        output = np.clip(output, 0, 255)
        return output.astype(np.uint8)

    
