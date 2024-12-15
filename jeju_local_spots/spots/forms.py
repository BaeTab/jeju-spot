import logging
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput
from .models import Spot, SpotImage

logger = logging.getLogger(__name__)

class MultipleFileInput(ClearableFileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs or {})
        self.attrs['multiple'] = 'multiple'

    def value_from_datadict(self, data, files, name):
        if files:
            return files.getlist(name)  # 모든 파일 반환
        return None

    def format_value(self, value):
        return None

class SpotForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control', 
            'accept': 'image/*',
            'name': 'images'
        }),
        required=True,  
        label='장소 이미지 (최소 1장, 최대 5장)'
    )

    class Meta:
        model = Spot
        fields = ['title', 'description', 'address', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            logger.info(f"SpotForm initialized with instance: {self.instance.id if self.instance.id else 'New'}")
            logger.debug(f"Form initialization details - Initial: {self.initial}, Data: {self.data}, Files: {len(self.files) if self.files else 0} files")
        except Exception as e:
            logger.error(f"Error initializing SpotForm: {str(e)}")
            raise

    def clean_images(self):
        logger.info("Starting image validation process")
        try:
            images = self.files.getlist('images')
            logger.info(f"Number of images submitted: {len(images)}")
            
            if not images:
                logger.warning("No images were uploaded")
                raise ValidationError("최소 1개의 이미지를 업로드해야 합니다.")
            
            for image in images:
                logger.debug(f"Validating image: {image.name} (Size: {image.size/1024/1024:.2f}MB, Type: {image.content_type})")
                
                if not image.content_type.startswith('image/'):
                    logger.error(f"Invalid file type uploaded: {image.content_type} for file {image.name}")
                    raise ValidationError(f"파일 {image.name}은(는) 이미지 파일이 아닙니다")
                
                if image.size > 5 * 1024 * 1024:
                    logger.error(f"File size too large: {image.size/1024/1024:.2f}MB for file {image.name}")
                    raise ValidationError(f"이미지 {image.name}의 크기가 5MB를 초과합니다")
            
            logger.info("Image validation completed successfully")
            return images
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during image validation: {str(e)}")
            raise ValidationError("이미지 처리 중 오류가 발생했습니다")

    def clean(self):
        logger.info("Starting form cleaning process")
        try:
            cleaned_data = super().clean()
            
            if 'images' in self.files:
                images = self.clean_images()
                logger.info(f"Successfully validated {len(images)} images")
                
                if len(images) > 5:
                    logger.error(f"Too many images uploaded: {len(images)}")
                    self.add_error('images', '최대 5장까지만 업로드 가능합니다.')
                
                cleaned_data['images'] = images
            else:
                logger.error("No images field in request.FILES")
                self.add_error('images', '이미지를 업로드해주세요.')
            
            logger.info("Form cleaning completed successfully")
            return cleaned_data
        except Exception as e:
            logger.error(f"Error during form cleaning: {str(e)}")
            raise

    def save(self, commit=True):
        logger.info("Starting spot save process")
        try:
            spot = super().save(commit=False)
            logger.info(f"Created spot instance: {spot.id if spot.id else 'New'}")
            
            if commit:
                spot.save()
                logger.info(f"Saved spot instance with ID: {spot.id}")
            
            images = self.files.getlist('images')
            logger.info(f"Processing {len(images)} images for spot")
            
            if images:
                for idx, image in enumerate(images, 1):
                    try:
                        spot_image = SpotImage.objects.create(spot=spot, image=image)
                        logger.info(f"Created SpotImage {idx}/{len(images)} with ID: {spot_image.id}")
                    except Exception as e:
                        logger.error(f"Error saving image {idx}/{len(images)}: {str(e)}")
                        raise
            else:
                logger.warning("No images to save for spot")
            
            logger.info(f"Successfully completed spot save process for ID: {spot.id}")
            return spot
        except Exception as e:
            logger.error(f"Error during spot save: {str(e)}")
            raise
