from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from shared.models import HistoryDates, ItemBase


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Course(HistoryDates):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses_created"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="courses"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    students = models.ManyToManyField(User, related_name="courses_joined", blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.order}. {self.title}"


class Content(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="contents"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["order"]


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    url = models.URLField()
    video = models.FileField(upload_to="videos", null=True)
