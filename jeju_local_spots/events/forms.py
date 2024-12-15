from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    title = forms.CharField(label='이벤트 제목', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='이벤트 설명', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    start_date = forms.DateField(label='시작 날짜', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(label='종료 날짜', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    location = forms.CharField(label='이벤트 장소', widget=forms.TextInput(attrs={'class': 'form-control'}))
    event_type = forms.ChoiceField(label='이벤트 유형', choices=Event.TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
    related_spot = forms.ModelChoiceField(label='관련 장소', queryset=None, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    discount_percentage = forms.IntegerField(label='할인율 (%)', required=False, min_value=0, max_value=100, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}))
    contact_info = forms.CharField(label='연락처 정보', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Event
        fields = [
            'title', 
            'description', 
            'start_date', 
            'end_date', 
            'location', 
            'event_type', 
            'related_spot', 
            'discount_percentage', 
            'contact_info'
        ]

    def __init__(self, *args, **kwargs):
        from spots.models import Spot
        super().__init__(*args, **kwargs)
        self.fields['related_spot'].queryset = Spot.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("종료 날짜는 시작 날짜보다 이후여야 합니다.")

        return cleaned_data
