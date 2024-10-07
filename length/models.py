# length/models.py

from django.db import models


class SegmentLengthImageModel(models.Model):
	"""Model for storing segmented image data and length results.

	Attributes:
		image_name (str): The name of the uploaded image.
		length_result (str): The estimated length of the pipe detected in the image.
		created_at (datetime): The timestamp when the image was uploaded and processed.
	"""
	
	image_name = models.CharField(max_length=255)
	length_result = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-created_at']
	
	def __str__(self):
		"""Returns a string representation of the SegmentLengthImageModel instance.

		Returns:
			str: A string displaying the image name and the length result.
		"""
		return f'{self.image_name} - {self.length_result}'
