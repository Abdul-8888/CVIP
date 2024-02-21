import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QHBoxLayout, QLineEdit, QDialog, QRadioButton, QButtonGroup
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PIL import Image, ImageQt
import numpy as np
from scipy.ndimage import uniform_filter

class ImageFilterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.filter_combobox.currentIndexChanged.connect(self.update_display)

    def initUI(self):
        # Widgets
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.path_label = QLabel("Image Path: ")
        self.path_textbox = QLineEdit(self)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_image)

        self.filter_label = QLabel("Select Filter:")
        self.filter_combobox = QComboBox(self)
        self.filter_combobox.addItems(["Original", "Laplacian Sharpening", "Mean Filter", "Negative", "Log Transformation", "Gamma Transformation", "Contrast Sketch", "Intensity Level Sketch"])

        # Layout
        layout = QVBoxLayout(self)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_textbox)
        path_layout.addWidget(self.browse_button)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_combobox)

        layout.addLayout(image_layout)
        layout.addLayout(path_layout)
        layout.addLayout(filter_layout)

        self.setLayout(layout)

        # Window settings
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Filter App')

    def browse_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp *.jpeg *.gif)')
        
        if file_path:
            self.path_textbox.setText(file_path)
            self.display_image(file_path)

    def display_image(self, file_path):
    # Read image using OpenCV
        image = cv2.imread(file_path)

        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert to QImage
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert to QPixmap and set to the QLabel
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def display_filtered_image(self, filtered_image):
        if len(filtered_image.shape) == 2:  # Grayscale image
            height, width = filtered_image.shape
            bytes_per_line = width
        elif len(filtered_image.shape) == 3:  # Color image
            height, width, channel = filtered_image.shape
            bytes_per_line = 3 * width

        qt_image = QImage(filtered_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def update_display(self):
        # Get the current selected filter
        selected_filter = self.filter_combobox.currentText()

        # Update the displayed image based on the selected filter
        if selected_filter == "Original":
            self.display_image(self.path_textbox.text())
        elif selected_filter == "Negative":
            # Apply negative filter to the original image
            image_path = self.path_textbox.text()
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            negative_image = self.apply_negative_filter(image)
            self.display_filtered_image(negative_image)
        elif selected_filter == "Log Transformation":
            # Apply log transformation filter to the original image
            image_path = self.path_textbox.text()
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            log_transformed_image = self.apply_log_transformation(image)
            self.display_filtered_image(log_transformed_image)
        elif selected_filter == "Canny Edge":
            # Apply your Canny edge filter or any other filter as needed
            pass
        elif selected_filter == "Mean Filter":
            # Apply mean filter to the original image
            image_path = self.path_textbox.text()
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            filtered_image = self.apply_mean_filter(image)
            self.display_filtered_image(filtered_image)
        elif selected_filter == "Laplacian Sharpening":
            # Apply Laplacian sharpening filter to the original image
            image_path = self.path_textbox.text()
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            sharpened_image = self.apply_laplacian_sharpening(image)
            self.display_filtered_image(sharpened_image)
        elif selected_filter == "Gamma Transformation":
            # Apply gamma transformation filter to the original image
            image_path = self.path_textbox.text()
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            gamma_corrected_image = self.apply_gamma_transformation(image, gamma=1.5)  # Adjust gamma value as needed
            self.display_filtered_image(gamma_corrected_image)
        elif selected_filter == "Contrast Sketch":
            # Apply contrast sketch filter to the original image
            image_path = self.path_textbox.text()
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            contrast_sketch_image = self.apply_contrast_sketch(image)
            self.display_filtered_image(contrast_sketch_image)
        elif selected_filter == "Intensity Level Sketch":
            # Apply intensity level sketch filter to the original image
            image_path = self.path_textbox.text()
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            intensity_level_sketch_image = self.apply_intensity_level_sketch(image)
            self.display_filtered_image(intensity_level_sketch_image)
    
    def apply_mean_filter(self, image):
        # Apply mean filter using scipy's uniform_filter
        filtered_image = uniform_filter(image, size=(3, 3, 1))
        return filtered_image
    
    def apply_laplacian_sharpening(self, image):
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        sharpened = cv2.addWeighted(image, 1.5, laplacian, -0.5, 0)
        return sharpened
    
    def apply_negative_filter(self, image):
        negative_image = 255 - image
        return negative_image
    
    def apply_log_transformation(self, image):
        c = 255 / np.log(1 + np.max(image))
        log_transformed = c * (np.log(image + 1))
        log_transformed = np.array(log_transformed, dtype=np.uint8)
        return log_transformed
    
    def apply_gamma_transformation(self, image, gamma=1.0):
        gamma_corrected = np.power(image / 255.0, 1.0 / gamma) * 255.0
        gamma_corrected = np.array(gamma_corrected, dtype=np.uint8)
        return gamma_corrected
    
    def apply_contrast_sketch(self, image):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Apply adaptive thresholding to create a binary sketch
        _, binary_sketch = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

        # Enhance contrast in the original image using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced = clahe.apply(gray)

        # Combine the binary sketch and contrast-enhanced image
        contrast_sketch = cv2.bitwise_and(contrast_enhanced, contrast_enhanced, mask=binary_sketch)

        return cv2.cvtColor(contrast_sketch, cv2.COLOR_GRAY2RGB)
    
    def apply_intensity_level_sketch(self, image, sketch_type="binary"):
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Initialize the sketch variable
        sketch = None

        # Create a popup window for sketch type selection
        dialog = QDialog(self)
        dialog.setWindowTitle("Intensity Level Sketch Options")

        # Create radio buttons for binary and brighten/darken options
        binary_button = QRadioButton("Binary Sketch", dialog)
        brighten_darken_button = QRadioButton("Brighten/Darken Sketch", dialog)

        # Create button group to ensure exclusive selection
        button_group = QButtonGroup(dialog)
        button_group.addButton(binary_button)
        button_group.addButton(brighten_darken_button)

        # Create layout and add radio buttons
        layout = QVBoxLayout(dialog)
        layout.addWidget(binary_button)
        layout.addWidget(brighten_darken_button)

        # Create OK button
        ok_button = QPushButton("OK", dialog)
        layout.addWidget(ok_button)

        # Set up signal/slot connections
        ok_button.clicked.connect(dialog.accept)

        # Show the dialog and wait for user input
        if dialog.exec_() == QDialog.Accepted:
            # Apply the selected sketch type
            if button_group.checkedButton() == binary_button:
                _, sketch = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
            elif button_group.checkedButton() == brighten_darken_button:
                # Adjust brightness based on sketch type
                if sketch_type == "brighten":
                    _, sketch = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
                    sketch = cv2.addWeighted(image, 1.5, cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB), 0.5, 0)
                elif sketch_type == "darken":
                    _, sketch = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
                    sketch = cv2.addWeighted(image, 0.5, cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB), 0.5, 0)

        # Ensure that sketch is not None
        if sketch is None:
            sketch = image

        return sketch
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageFilterApp()
    ex.show()
    sys.exit(app.exec_())
