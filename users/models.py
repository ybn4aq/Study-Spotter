import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    study_spot_parent = models.ForeignKey("StudySpot", on_delete=models.CASCADE)
    message = models.CharField(max_length=1000, default="")
    upvotes = models.IntegerField(default=0)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    upvoted_by = models.ManyToManyField(
        User, related_name="upvoted_comments"
    )  # stores which users have upvoted

    def __str__(self):
        return self.message


class StudySpot(models.Model):
    building_name = models.CharField(max_length=200)
    user_posted = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    notes = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    latitude = models.FloatField(blank=True, null=True, default="0.0")
    longitude = models.FloatField(blank=True, null=True, default="0.0")
    liked_by = models.ManyToManyField(
        User, related_name="liked_spots"
    )  # list of users that have liked it
    comments = models.ManyToManyField(Comment, related_name="comments")

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.building_name

    def user_has_liked(self, user):
        return self.liked_by.filter(pk=user.pk).exists()
