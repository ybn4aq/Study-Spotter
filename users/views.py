from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import StudySpot, Comment
from django.utils import timezone
from .forms import StudySpotForm, CommentForm
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render


def logout_view(request):
    logout(request)
    return redirect("/")


class StudySpotCreateView(generic.CreateView):
    template_name = "add_study_spot.html"
    model = StudySpot
    form_class = StudySpotForm
    success_url = reverse_lazy("users:home")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            study_spot = form.save(commit=False)
            study_spot.user_posted = self.request.user
            study_spot.pub_date = timezone.now()
            study_spot.likes = 0
            if (
                not study_spot.building_name
                or not study_spot.latitude
                or not study_spot.longitude
            ):
                return HttpResponseBadRequest(
                    "Building Name, Latitude, and Longitude are required."
                )
            study_spot.save()
            study_spot.approved = False
            study_spot.save()
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        all_study_spots = self.get_queryset()
        locations = []
        for i in all_study_spots.filter(approved=True):
            try:
                lat = float(i.latitude)
                long = float(i.longitude)
            except (ValueError, TypeError):
                continue
            data = {
                "lat": lat,
                "long": long,
                "name": i.building_name,
                "url": reverse("users:spot", kwargs={"pk": i.id}),
                "likes": i.likes,
            }
            locations.append(data)
        context = {
            "locations": locations,
            "lat_default": float(38.03541960020662),
            "lng_default": float(-78.50353079158717),
        }
        context["lat_default"] = 38.03541960020662
        context["lng_default"] = -78.5035307915871
        context["solo"] = 0
        context["spot_name"] = "meep"
        return context


class StudySpotAggregateView(generic.ListView):
    model = StudySpot
    template_name = "all_study_spots.html"
    context_object_name = "all_study_spots"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_study_spots = StudySpot.objects.order_by("-likes")
        context["all_study_spots"] = latest_study_spots
        context["is_user_admin"] = self.request.user.is_superuser
        user_has_liked = {}
        for spot in latest_study_spots:
            # user_has_liked[spot.pk] = user has liked this spot
            user_has_liked[spot.pk] = spot.liked_by.filter(
                pk=self.request.user.pk
            ).exists()
        context["user_has_liked"] = user_has_liked
        return context

    def post(self, request):
        if self.request.user.is_authenticated:
            action = self.request.POST.get("action")
            study_spot_id = self.request.POST.get("study_spot_id")
            study_spot = StudySpot.objects.get(pk=study_spot_id)
            if action == "delete":
                if self.request.user.is_superuser:
                    study_spot.delete()
            elif action == "like":
                if not study_spot.liked_by.filter(pk=self.request.user.pk).exists():
                    study_spot.likes += 1
                    study_spot.liked_by.add(self.request.user.pk)
                    study_spot.save()
            else:  # action == "unlike"
                if study_spot.liked_by.filter(pk=self.request.user.pk).exists():
                    study_spot.likes -= 1
                    study_spot.liked_by.remove(self.request.user.pk)
                    study_spot.save()
            return HttpResponseRedirect(reverse_lazy("users:study_spots"))
        return HttpResponseBadRequest("Must be logged in.")


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        most_popular_spot = StudySpot.objects.order_by("-likes").first()
        context = {"spot": most_popular_spot}
        return context


class MapView(generic.TemplateView):
    model = StudySpot
    template_name = "main-map.html"
    context_object_name = "locations"

    def get_queryset(self):
        return StudySpot.objects.all()

    def get(self, request):
        all_study_spots = self.get_queryset()
        locations = []
        for i in all_study_spots.filter(approved=True):
            try:
                lat = float(i.latitude)
                long = float(i.longitude)
            except (ValueError, TypeError):
                continue
            data = {
                "lat": lat,
                "long": long,
                "name": i.building_name,
                "url": reverse("users:spot", kwargs={"pk": i.id}),
                "likes": i.likes,
            }
            locations.append(data)
        context = {"locations": locations}
        return render(request, self.template_name, context)


class StudySpotApproveView(generic.ListView):
    model = StudySpot
    template_name = "approve_spots.html"
    context_object_name = "latest_study_spots"

    def get_queryset(self):
        return StudySpot.objects.filter(approved=False).order_by("-pub_date")

    def post(self, request):
        if self.request.user.is_superuser:
            study_spot_id = request.POST.get("study_spot_id")
            action = request.POST.get("action")
            if study_spot_id and action:
                study_spot = StudySpot.objects.get(pk=study_spot_id)
                if action == "approve":
                    study_spot.approved = True
                    study_spot.save()
                elif action == "delete":
                    study_spot.delete()
        return redirect("users:approve_spots")


class SoloStudySpotView(generic.DetailView):
    model = StudySpot
    template_name = "solo_study_spot.html"
    context_object_name = "spot"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        study_spot_id = self.kwargs.get("pk")
        study_spot = StudySpot.objects.get(pk=study_spot_id)
        latest_study_spots = StudySpot.objects.order_by("-pub_date")
        comments = Comment.objects.filter(study_spot_parent=study_spot).order_by(
            "-upvotes"
        )
        context["all_study_spots"] = latest_study_spots
        context["is_user_admin"] = self.request.user.is_superuser
        context["comments"] = comments
        context["lat_default"] = float(study_spot.latitude)
        context["lng_default"] = float(study_spot.longitude)
        all_study_spots = self.get_queryset()
        locations = []
        for i in all_study_spots.filter(approved=True): 
            try:
                lat = float(i.latitude)
                long = float(i.longitude)
            except (ValueError, TypeError):
                continue
            data = {
                "lat": lat,
                "long": long,
                "name": i.building_name,
                "url": reverse("users:spot", kwargs={"pk": i.id}),
                "likes": i.likes,
            }

            locations.append(data)
        context["locations"] = locations
        context["lat_default"] = data
        user_has_liked = {}
        for spot in latest_study_spots:
            # user_has_liked[spot.pk] = user has liked this spot
            user_has_liked[spot.pk] = spot.liked_by.filter(
                pk=self.request.user.pk
            ).exists()
        user_has_upvoted = {}
        for comment in comments:
            user_has_upvoted[comment.pk] = comment.upvoted_by.filter(
                pk=self.request.user.pk
            ).exists()
        context["user_has_liked"] = user_has_liked
        context["user_has_upvoted"] = user_has_upvoted
        context[
            "lat_default"
        ] = (
            study_spot.latitude
        )  #  I couldn't tell you why it works like this. whatever.
        context["solo"] = 1
        context["spot_name"] = study_spot.building_name
        return context

    def post(self, request, **kwargs):
        if self.request.user.is_authenticated:
            action = self.request.POST.get("action")
            study_spot_id = self.request.POST.get("study_spot_id")
            if action == "delete":
                study_spot = StudySpot.objects.get(pk=study_spot_id)
                if self.request.user.is_superuser:
                    study_spot.delete()
                    return HttpResponseRedirect(reverse_lazy("users:study_spots"))
            elif action == "like":
                study_spot = StudySpot.objects.get(pk=study_spot_id)
                if not study_spot.liked_by.filter(pk=self.request.user.pk).exists():
                    study_spot.likes += 1
                    study_spot.liked_by.add(self.request.user.pk)
                    study_spot.save()
            elif action == "unlike":
                study_spot = StudySpot.objects.get(pk=study_spot_id)
                if study_spot.liked_by.filter(pk=self.request.user.pk).exists():
                    study_spot.likes -= 1
                    study_spot.liked_by.remove(self.request.user.pk)
                    study_spot.save()
            elif action == "comment":
                form = CommentForm(self.request.POST)
                if form.is_valid():
                    new_comment = form.save(commit=False)
                    new_comment.poster = self.request.user
                    study_spot = StudySpot.objects.get(pk=study_spot_id)
                    new_comment.study_spot_parent = study_spot
                    new_comment.message = form.cleaned_data["message"]
                    if not new_comment.message:
                        return HttpResponseBadRequest("Comment field is required.")
                    new_comment.save()
                    study_spot.comments.add(new_comment)
                    study_spot.save()
            elif action == "upvote":
                comment_id = self.request.POST.get("comment_id")
                comment = Comment.objects.get(pk=comment_id)
                if not comment.upvoted_by.filter(pk=self.request.user.pk).exists():
                    comment.upvoted_by.add(self.request.user.pk)
                    comment.upvotes += 1
                    comment.save()
                study_spot_id = comment.study_spot_parent.pk
            elif action == "un_upvote":
                comment_id = self.request.POST.get("comment_id")
                comment = Comment.objects.get(pk=comment_id)
                if comment.upvoted_by.filter(pk=self.request.user.pk).exists():
                    comment.upvoted_by.remove(self.request.user.pk)
                    comment.upvotes -= 1
                    comment.save()
                study_spot_id = comment.study_spot_parent.pk
            else:  # action == "comment_delete":
                comment_id = self.request.POST.get("comment_id")
                comment = Comment.objects.get(pk=comment_id)
                study_spot_id = comment.study_spot_parent.pk
                if self.request.user.is_superuser:
                    comment.delete()
            return redirect("users:spot", pk=study_spot_id)
