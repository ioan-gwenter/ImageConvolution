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

        # ---------------------------
        #       IMAGE DATA
        # ---------------------------
        
        self.__padded_image_data = None
        self.__smoothed_image_data = None

        self.__horizontal_edge_image_data = None
        self.__vertical_edge_image_data = None
        self.__edge_strength_image_data = None

        # ---------------------------
        #       KERNERL VAR
        # ---------------------------

        self.available_smoothing_kernels = ["Gaussian", "Average", "Custom"]
        self.current_smoothing_kernel = None

        self.__sobel_x = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
        self.__sobel_y = [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]


    # ---------------------------
    #       KERNEL MANAGER
    # ---------------------------

    def get_available_kernels(self) -> List:
        return self.available_smoothing_kernels

    def get_current_kernel(self) -> List:
        return self.current_smoothing_kernel
    
    def update_kernel(self, kernel_type: str, **params) -> None:
        """
        Updates the current kernel based on the selected type and parameters.
        
        :param kernel_type: The type of kernel .
        :param params: Additional parameters required for the kernel.
        """
        if kernel_type == "Gaussian":
            size = params.get("size")
            sigma = params.get("sigma")
            self.current_smoothing_kernel = self.__generate_gaussian_kernel(size, sigma)
        elif kernel_type == "Average":
            size = params.get("size")
            self.current_smoothing_kernel = self.__generate_average_kernel(size)
        else:
            self.current_smoothing_kernel = None
            raise ValueError(f"Unsupported kernel type: {kernel_type}")

    def __generate_gaussian_kernel(self, size: int, sigma: float) -> List[List[float]]:
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

        return np.ndarray.tolist(gaussian_kernel)
    
    def __generate_average_kernel(self, size: int) -> List[List[float]]:
        """
        Generates an averaging kernel of given size.

        :param size: The size of the kernel (size x size).
        :return: A 2D NumPy array representing the averaging kernel.
        """
        if size % 2 == 0:
            raise ValueError("Kernel size must be an odd integer to ensure a center pixel.")

        # Create an NxN matrix filled with 1s
        kernel = [[1] * size for _ in range (size)]

        # Normalize by dividing each element by the total number of elements
        kernel /= (size * size)

        print(kernel)

        return np.ndarray.tolist(kernel)
        
    def __pad_image(self, kernel_size: int, image: List[List[int]]) -> List[List[int]]:

        if not image or not image[0]:
            raise ValueError("Input image cannot be empty")

        if kernel_size < 1 or kernel_size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer")

        img_height = len(image)
        img_width = len(image[0])
        pad_size = kernel_size // 2

        # create a padded zeroed array for the image
        padded_image = [[0] * (img_width + 2 * pad_size) for _ in range(img_height + 2 * pad_size)]

        # Copy the image over to the array
        for row in range(img_height):
            for col in range(img_width):
                padded_image[row + pad_size][col + pad_size] = image[row][col]

        return padded_image
    



    def __apply_kernel(self, kernel:List[List[int]]) -> List[List[int]]:
        """
        Applies a convolutional kernel to the image.
        :param kernel: Kernel 2D matrix.
        :return: Processed 2D array.
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
            self.input_image_data = self.__load_image_grayscale(file_path=file_path)
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
        
    def __save_image(self, output_path: str, image_array: List[List[int]]) -> None:
        """
        Saves an image to the specified file path.
        :param output_path: File path to save the image.
        :param image_array: 2D array to save.
        """
        return cv2.imwrite(output_path, image_array)

    def __load_image_grayscale(self, file_path: str) -> List[List[int]]:
        """
        Loads an image as a 2D array in grayscale.
        :param file_path: Path to the image file.
        :return: 2D  array representing pixel intensities (0-255).
        """
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        
        if image is None:
            raise ValueError(f"Failed to load image: {file_path}")
        
        return image.tolist()

    
