from django import forms
from .models import StudySpot, Comment


class StudySpotForm(forms.ModelForm):
    class Meta:
        model = StudySpot
        fields = [
            "building_name",
            "pub_date",
            "user_posted",
            "notes",
            "likes",
            "approved",
            "latitude",
            "longitude",
            "comments",
        ]
        exclude = [
            "pub_date",
            "user_posted",
            "likes",
            "approved",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        super(StudySpotForm, self).__init__(*args, **kwargs)
        self.fields["building_name"].required = True
        self.fields["latitude"].required = True
        self.fields["longitude"].required = True
        self.fields["notes"].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["study_spot_parent", "message", "upvotes", "poster", "upvoted_by"]
        exclude = ["study_spot_parent", "upvotes", "poster", "upvoted_by"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["message"].required = True
