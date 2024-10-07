# length/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from .forms import ImageUploadForm
from .segment_pipe import Segmentation
from .length_pipe_estimate import DistanceCalculator
from django.views.generic import TemplateView
from django.utils import timezone
from .models import SegmentLengthImageModel
from datetime import timedelta


class PipeLengthView(LoginRequiredMixin, FormView):
	"""
	View to handle the uploading of an image and calculating the pipe length.

	Attributes:
		template_name (str): The name of the template to render.
		form_class (Form): The form used to upload an image.
		success_url (str): URL to redirect to upon successful form submission.
	"""
	template_name = 'length/length.html'
	form_class = ImageUploadForm
	success_url = reverse_lazy('length:length')
	login_url = reverse_lazy(
		'accounts:user_login')  # Redirect to login if not authenticated
	
	def form_valid(self, form):
		"""
		Handle a valid form submission.

		Args:
			form (ImageUploadForm): The submitted form with an uploaded image.

		Returns:
			HttpResponse: Rendered response with the length result and segmented image path.
		"""
		try:
			# Get the uploaded image from the form
			uploaded_image = form.cleaned_data['image']
			
			# Initialize the segmentation process
			seg_result = Segmentation(settings.SEGMENTATION_MODEL)
			
			# Segment the image and get points x1 and x2
			segmentation_output = seg_result.segment_image(uploaded_image)
			
			# Check if segmentation_output is None
			if segmentation_output is None:
				raise Exception(
					"Segmentation failed, no pipe detected in the image.")
			
			x1, x2, segmented_image = segmentation_output
			
			# Calculate the length between the two points
			length_estimate = DistanceCalculator(settings.COORDINATES,
			                                     settings.DISTANCE_PER_INTERVAL)
			total_length = length_estimate.calculate_length_between_any_two_points(
				x1, x2)
			
			# Save the segmented result image
			result_image = seg_result.get_result_image()
			if result_image:
				result_image_name = f"segmented_{uploaded_image.name}"
				default_storage.save(result_image_name,
				                     ContentFile(result_image))
			else:
				raise Exception("Segmentation failed, no image to save.")
		
		except Exception as e:
			form.add_error(None, f"An error occurred: {str(e)}")
			return self.form_invalid(form)
		
		# Save the result in the database
		SegmentLengthImageModel.objects.create(
			image_name=uploaded_image.name,
			length_result=f'{total_length}',
		)
		
		# Prepare the context for rendering the response
		context = {
			'total_length': total_length,
			'form': form,
			'result_image_path': f"{settings.MEDIA_URL}{result_image_name}",
		}
		return self.render_to_response(context)
	
	def form_invalid(self, form):
		"""
		Handle an invalid form submission.

		Args:
			form (ImageUploadForm): The submitted form that has errors.

		Returns:
			HttpResponse: Rendered response with the form containing errors.
		"""
		return self.render_to_response({'form': form})


class PipeLengthListView(LoginRequiredMixin, TemplateView):
	"""
	View to display a list of processed images and their length measurements.

	Attributes:
		template_name (str): The name of the template to render.
	"""
	template_name = 'length/length_list.html'
	
	def get_context_data(self, **kwargs):
		"""
		Add context data for rendering the list of images.

		Args:
			kwargs: Additional keyword arguments.

		Returns:
			dict: Context data including images and selected filter.
		"""
		context = super().get_context_data(**kwargs)
		filter_param = self.request.GET.get('filter', 'all')
		
		# Filter based on the selected option
		if filter_param == 'today':
			images = SegmentLengthImageModel.objects.filter(
				created_at__date=timezone.now().date())
		elif filter_param == 'yesterday':
			yesterday = timezone.now().date() - timedelta(days=1)
			images = SegmentLengthImageModel.objects.filter(
				created_at__date=yesterday)
		elif filter_param == 'this_week':
			start_of_week = timezone.now().date() - timedelta(
				days=timezone.now().date().weekday())
			images = SegmentLengthImageModel.objects.filter(
				created_at__date__gte=start_of_week)
		else:
			images = SegmentLengthImageModel.objects.all()
		
		context['images'] = images
		context['filter'] = filter_param
		
		return context
