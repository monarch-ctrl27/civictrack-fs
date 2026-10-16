from urllib.parse import urlencode

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import charts
from .ai import suggest_category
from .constants import (
    AUTO_CATEGORY_VALUE,
    CATEGORIES,
    CATEGORY_MAP,
    DISTRICTS,
    STATUS_CHOICES,
)
from .forms import CommentForm, MapFilterForm, ReportForm, StatusUpdateForm
from .models import Report


def _role(request):
    """Session-based role switch (Resident / Municipal official).

    This is a demo convenience, not authentication — it lets judges try
    both experiences without needing to build a login system for the
    hackathon. Swap this for real auth + permissions before production
    use (see README "Before you deploy").
    """
    return request.session.get("role", "resident")


def set_role(request):
    role = request.GET.get("role")
    if role in ("resident", "official"):
        request.session["role"] = role
    next_url = request.GET.get("next") or reverse("issues:home")
    return redirect(next_url)


def home(request):
    reports = Report.objects.all()
    context = {
        "role": _role(request),
        "total_reports": reports.count(),
        "resolved_reports": reports.filter(status="resolved").count(),
        "district_count": len(DISTRICTS),
        "category_count": len(CATEGORIES) - 1,  # exclude "Other"
    }
    return render(request, "issues/home.html", context)


def report_create(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            detected_note = None
            if report.category == AUTO_CATEGORY_VALUE:
                suggested = suggest_category(report.description)
                report.category = suggested or "other"
                detected_note = CATEGORY_MAP[report.category]["label"]
            report.votes = 1
            report.save()

            voted = request.session.get("voted_reports", [])
            voted.append(report.id)
            request.session["voted_reports"] = voted

            if detected_note:
                messages.success(
                    request,
                    f"Report submitted. CivicTrack automatically categorised this "
                    f"as \u201c{detected_note}\u201d — you can change it any time in "
                    f"the Django admin.",
                )
            else:
                messages.success(request, "Report submitted — thank you.")
            return redirect("issues:map_feed")
    else:
        form = ReportForm(initial={"category": AUTO_CATEGORY_VALUE})

    return render(request, "issues/report_form.html", {"form": form, "role": _role(request)})


def _apply_filters(request, queryset):
    """Validate the category/status/district query params against the
    known choices (via MapFilterForm) before touching the database, then
    filter the queryset. Anything invalid or missing quietly falls back
    to "all" rather than raising an error.
    """
    filter_form = MapFilterForm(request.GET)
    filter_form.is_valid()  # populates cleaned_data even for partial input
    category = filter_form.cleaned_data.get("category") or "all"
    status = filter_form.cleaned_data.get("status") or "all"
    district = filter_form.cleaned_data.get("district") or "all"

    if category != "all":
        queryset = queryset.filter(category=category)
    if status != "all":
        queryset = queryset.filter(status=status)
    if district != "all":
        queryset = queryset.filter(district=district)
    return queryset, {"category": category, "status": status, "district": district}


def map_feed(request):
    reports, active_filters = _apply_filters(request, Report.objects.all())
    role = _role(request)

    base_url = reverse("issues:map_feed")

    def url_with(**overrides):
        params = dict(active_filters)
        params.update(overrides)
        params = {k: v for k, v in params.items() if v and v != "all"}
        query = urlencode(params)
        return f"{base_url}?{query}" if query else base_url

    districts_with_state = []
    for d in DISTRICTS:
        is_active = active_filters["district"] == d["id"]
        x1, y1, x2, y2 = d["box"]
        districts_with_state.append(
            {
                **d,
                "active": is_active,
                "toggle_url": url_with(district="all" if is_active else d["id"]),
                "box_width": x2 - x1,
                "box_height": y2 - y1,
                "label_x": x1 + (x2 - x1) / 2,
                "label_y": y1 + (y2 - y1) / 2 - 4,
                "sub_y": y1 + (y2 - y1) / 2 + 12,
            }
        )

    voted_reports = set(request.session.get("voted_reports", []))

    context = {
        "role": role,
        "reports": reports,
        "categories": CATEGORIES,
        "districts": districts_with_state,
        "statuses": STATUS_CHOICES,
        "active_filters": active_filters,
        "voted_reports": voted_reports,
        "next_url": request.get_full_path(),
    }
    return render(request, "issues/map_feed.html", context)


@require_POST
def vote(request, pk):
    report = get_object_or_404(Report, pk=pk)
    voted_reports = request.session.get("voted_reports", [])
    if pk in voted_reports:
        voted_reports.remove(pk)
        report.votes = max(0, report.votes - 1)
    else:
        voted_reports.append(pk)
        report.votes += 1
    report.save(update_fields=["votes"])
    request.session["voted_reports"] = voted_reports
    return redirect(request.POST.get("next") or "issues:map_feed")


@require_POST
def comment_add(request, pk):
    report = get_object_or_404(Report, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid() and form.cleaned_data["text"].strip():
        comment = form.save(commit=False)
        comment.report = report
        comment.author_name = "Municipal official" if _role(request) == "official" else "Resident"
        comment.save()
    return redirect(request.POST.get("next") or "issues:map_feed")


@require_POST
def status_update(request, pk):
    if _role(request) != "official":
        messages.error(request, "Switch to \u201cMunicipal official\u201d to update a status.")
        return redirect(request.POST.get("next") or "issues:map_feed")

    report = get_object_or_404(Report, pk=pk)
    form = StatusUpdateForm(request.POST, instance=report)
    if form.is_valid():
        form.save()
        messages.success(request, f"\u201c{report.title}\u201d marked as {report.get_status_display()}.")
    return redirect(request.POST.get("next") or "issues:map_feed")


def dashboard(request):
    reports = Report.objects.all()
    role = _role(request)

    by_district = (
        reports.values("district").annotate(n=Count("id")).order_by("-n")
    )
    top_district = None
    if by_district:
        top_id = by_district[0]["district"]
        top_district = next((d for d in DISTRICTS if d["id"] == top_id), None)

    context = {
        "role": role,
        "reports": reports,
        "total_reports": reports.count(),
        "resolved_reports": reports.filter(status="resolved").count(),
        "open_reports": reports.exclude(status="resolved").count(),
        "top_district": top_district,
        "statuses": STATUS_CHOICES,
        "category_chart": charts.category_bar_chart(reports),
        "district_chart": charts.district_bar_chart(reports),
        "status_chart": charts.status_donut_chart(reports),
        "trend_chart": charts.trend_line_chart(reports),
    }
    return render(request, "issues/dashboard.html", context)
