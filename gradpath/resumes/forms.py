from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'summary', 'skills', 'education', 'experience', 'certifications', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Job Title (Optional)'}),
            'summary': forms.Textarea(attrs={'placeholder': 'Enter Summary (Optional)', 'rows': 3}),
            'skills': forms.Textarea(attrs={'placeholder': 'Enter Skills (Optional)', 'rows': 3}),
            'education': forms.Textarea(attrs={'placeholder': 'Enter Education (Optional)', 'rows': 3}),
            'experience': forms.Textarea(attrs={'placeholder': 'Enter Experience (Optional)', 'rows': 3}),
            'certifications': forms.Textarea(attrs={'placeholder': 'Enter Certifications (Optional)', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pdf_file = cleaned_data.get("pdf_file")
        other_fields = ['title', 'summary', 'skills', 'education', 'experience', 'certifications']
        filled = any(cleaned_data.get(field) for field in other_fields)

        if not filled and not pdf_file:
            raise forms.ValidationError("Either upload a PDF or fill in at least one field.")
        return cleaned_data
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            # Check file size (5MB limit)
            if pdf_file.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("The uploaded file is too large (max 5MB).")
            return pdf_file
        else:
            return None # No file uploaded, return None
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Custom save logic if needed
        if commit:
            instance.save()
        return instance
