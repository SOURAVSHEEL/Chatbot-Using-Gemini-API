from django import forms

class GeminiProVisionForm(forms.Form):
    input_text = forms.CharField(label='Input Prompt', required=False)
    image = forms.ImageField(label="Upload an image", required=False)
