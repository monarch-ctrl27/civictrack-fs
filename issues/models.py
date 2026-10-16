import random

from django.db import models
from django.utils import timezone

from .constants import (
    CATEGORY_CHOICES,
    CATEGORY_MAP,
    DISTRICT_CHOICES,
    DISTRICT_MAP,
    STATUS_CHOICES,
    STATUS_COLORS,
    STATUS_SOFT_COLORS,
)


def random_point_in_district(district_id):
    """Pick a pseudo-random (x, y) point inside a district's map box.

    Used so each report gets a stable marker position on the SVG map
    without needing real GPS coordinates for this prototype. Swap this
    out for real latitude/longitude plus a proper map tile provider
    when integrating a production GIS layer.
    """
    box = DISTRICT_MAP[district_id]["box"]
    x1, y1, x2, y2 = box
    x = random.randint(x1 + 18, x2 - 18)
    y = random.randint(y1 + 16, y2 - 16)
    return x, y


class Report(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    district = models.CharField(max_length=30, choices=DISTRICT_CHOICES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="reported"
    )
    reporter_name = models.CharField(
        max_length=60,
        blank=True,
        help_text="Leave blank to report anonymously.",
    )
    photo = models.ImageField(upload_to="reports/", blank=True, null=True)
    votes = models.PositiveIntegerField(default=1)
    map_x = models.PositiveIntegerField(default=0)
    map_y = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Give every new report a stable map marker position the first
        # time it is saved.
        if not self.pk and not (self.map_x and self.map_y):
            self.map_x, self.map_y = random_point_in_district(self.district)
        super().save(*args, **kwargs)

    @property
    def category_label(self):
        return CATEGORY_MAP.get(self.category, {}).get("label", self.category)

    @property
    def category_color(self):
        return CATEGORY_MAP.get(self.category, {}).get("color", "#566573")

    @property
    def district_name(self):
        return DISTRICT_MAP.get(self.district, {}).get("name", self.district)

    @property
    def status_color(self):
        return STATUS_COLORS.get(self.status, "#2B4570")

    @property
    def status_soft_color(self):
        return STATUS_SOFT_COLORS.get(self.status, "#DCE4F0")


class Comment(models.Model):
    report = models.ForeignKey(
        Report, related_name="comments", on_delete=models.CASCADE
    )
    author_name = models.CharField(max_length=60, default="Resident")
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author_name}: {self.text[:40]}"
