from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': '리뷰를 작성해주세요 (최대 1000자)'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 1000:
            raise forms.ValidationError("리뷰는 1000자 이내로 작성해주세요.")
        return content
