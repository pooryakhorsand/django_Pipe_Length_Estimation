# length/segment_pipe.py

from ultralytics import YOLO
import cv2
import numpy as np


class Segmentation:
	"""Class for segmenting images using a YOLO model.

	Attributes:
		model_path (str): Path to the trained YOLO model.
		result_image (np.ndarray): Resulting image after segmentation.
	"""
	
	def __init__(self, model_path):
		"""Initializes the Segmentation class with a YOLO model path.

		Args:
			model_path (str): Path to the YOLO model file.
		"""
		self.model_path = model_path
		self.result_image = None
	
	def segment_image(self, uploaded_file):
		"""Segments the uploaded image to detect objects using the YOLO model.

		Args:
			uploaded_file (file-like object): The uploaded image file to segment.

		Returns:
			tuple: A tuple containing the minimum and maximum x-coordinates of
				   the detected objects, and the results from the YOLO model,
				   or None if no objects are detected or if segmentation fails.
		"""
		model = YOLO(self.model_path)
		file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
		image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
		
		if image is None:
			print("Error: Could not decode the image.")
			return None
		
		results = model.predict(image, save=False, conf=0.5)
		x_coordinates = []
		
		if results:
			for result in results:
				if result.masks is not None:
					masks = result.masks.data
					
					for mask in masks:
						mask_np = mask.numpy().astype(np.uint8)
						mask_resized = cv2.resize(mask_np, (
						image.shape[1], image.shape[0]),
						                          interpolation=cv2.INTER_LINEAR)
						
						y_indices, x_indices = np.where(mask_resized > 0)
						if len(x_indices) == 0 or len(y_indices) == 0:
							print("No valid indices found in the mask")
							continue  # Skip if no indices are found
						
						x_coordinates.extend(x_indices.tolist())
						
						# Create a color image for visualization
						colored_mask = cv2.cvtColor(mask_resized,
						                            cv2.COLOR_GRAY2BGR)
						self.result_image = cv2.addWeighted(image, 0.5,
						                                    colored_mask, 0.5,
						                                    0)
		
		if x_coordinates:
			return min(x_coordinates), max(x_coordinates), results
		else:
			print(
				"No segmentation performed, no objects detected in the image.")
			return None
	
	def get_result_image(self):
		"""Retrieves the resulting segmented image.

		Returns:
			bytes: The resulting segmented image in PNG format, or None if
				   no result image exists.
		"""
		if self.result_image is not None:
			_, buffer = cv2.imencode('.png', self.result_image)
			return buffer.tobytes()
		return None
