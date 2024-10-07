# length/forms.py

from django import forms


class ImageUploadForm(forms.Form):
	"""Form for uploading an image.

	This form contains a single field for the user to upload an image file.
	The uploaded image will be processed for pipe length estimation.
	"""
	
	image = forms.ImageField(required=True, label='Upload Image')
	"""
	image (ImageField): A field for the user to upload an image.

	This field is required and will not accept empty submissions.
	The uploaded file must be an image format supported by the server.
	"""
