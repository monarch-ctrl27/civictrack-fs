from django import forms

from .constants import AUTO_CATEGORY_VALUE, CATEGORY_CHOICES, DISTRICT_CHOICES, STATUS_CHOICES
from .models import Comment, Report

MAX_PHOTO_SIZE_MB = 5


class ReportForm(forms.ModelForm):
    # "Auto-detect" is added in front of the real categories so residents
    # who don't know municipal terminology can let the classifier in
    # ai.py choose for them.
    category = forms.ChoiceField(
        choices=[(AUTO_CATEGORY_VALUE, "Let CivicTrack suggest a category")]
        + CATEGORY_CHOICES,
        label="Category",
    )

    class Meta:
        model = Report
        fields = ["title", "description", "category", "district", "reporter_name", "photo"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Pothole outside the clinic on Voortrekker Street",
                    "maxlength": 120,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the problem, how long it has been going on, "
                    "and who it affects.",
                    "rows": 5,
                }
            ),
            "district": forms.Select(),
            "reporter_name": forms.TextInput(
                attrs={"placeholder": "Leave blank to report anonymously"}
            ),
        }
        labels = {
            "title": "Issue title",
            "description": "What's happening?",
            "district": "District",
            "reporter_name": "Your name (optional)",
            "photo": "Photo evidence (optional)",
        }

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo:
            content_type = getattr(photo, "content_type", "") or ""
            if not content_type.startswith("image/"):
                raise forms.ValidationError("Please upload an image file.")
            if photo.size > MAX_PHOTO_SIZE_MB * 1024 * 1024:
                raise forms.ValidationError(
                    f"Image must be smaller than {MAX_PHOTO_SIZE_MB}MB."
                )
        return photo

    def clean_description(self):
        description = self.cleaned_data.get("description", "").strip()
        if len(description) < 10:
            raise forms.ValidationError(
                "Please add a little more detail (at least 10 characters)."
            )
        return description


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(
                attrs={"placeholder": "Add a comment", "maxlength": 280}
            )
        }
        labels = {"text": ""}


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["status"]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label="")


class MapFilterForm(forms.Form):
    """Not rendered directly (the template builds its own <select> tags so
    it can auto-submit via GET), but kept here as the single source of
    truth for which filter values are valid.
    """

    category = forms.ChoiceField(
        choices=[("all", "All categories")] + CATEGORY_CHOICES, required=False
    )
    status = forms.ChoiceField(
        choices=[("all", "All statuses")] + STATUS_CHOICES, required=False
    )
    district = forms.ChoiceField(
        choices=[("all", "All districts")] + DISTRICT_CHOICES, required=False
    )
