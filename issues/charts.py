"""
Server-side chart rendering for the municipal dashboard.

Charts are drawn with matplotlib and returned as base64-encoded PNGs so
templates can embed them with a plain <img src="data:image/png;base64,...">
tag. This keeps the whole project to Python + Django + HTML/CSS, with no
JavaScript charting library required.
"""
import base64
import io

import matplotlib

matplotlib.use("Agg")  # headless backend — required when rendering inside Django

import matplotlib.pyplot as plt
import pandas as pd

from .constants import CATEGORIES, DISTRICTS, STATUS_CHOICES, STATUS_COLORS

INK_SOFT = "#4B5A52"
LINE_COLOR = "#DDD2B7"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "text.color": INK_SOFT,
        "axes.edgecolor": LINE_COLOR,
        "axes.labelcolor": INK_SOFT,
        "xtick.color": INK_SOFT,
        "ytick.color": INK_SOFT,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
    }
)


def _fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", transparent=True)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def category_bar_chart(reports_queryset):
    counts = {c["id"]: 0 for c in CATEGORIES}
    for report in reports_queryset:
        counts[report.category] = counts.get(report.category, 0) + 1

    labels = [c["label"] for c in CATEGORIES]
    values = [counts[c["id"]] for c in CATEGORIES]
    colors = [c["color"] for c in CATEGORIES]

    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.bar(labels, values, color=colors, width=0.6)
    ax.set_ylabel("Reports")
    ax.tick_params(axis="x", labelrotation=30, labelsize=8)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    fig.tight_layout()
    return _fig_to_base64(fig)


def district_bar_chart(reports_queryset):
    counts = {d["id"]: 0 for d in DISTRICTS}
    for report in reports_queryset:
        counts[report.district] = counts.get(report.district, 0) + 1

    labels = [d["name"] for d in DISTRICTS]
    values = [counts[d["id"]] for d in DISTRICTS]

    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.barh(labels, values, color="#2B4570", height=0.55)
    ax.invert_yaxis()
    ax.set_xlabel("Reports")
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    fig.tight_layout()
    return _fig_to_base64(fig)


def status_donut_chart(reports_queryset):
    counts = {status_id: 0 for status_id, _ in STATUS_CHOICES}
    for report in reports_queryset:
        counts[report.status] = counts.get(report.status, 0) + 1

    labels = [label for _, label in STATUS_CHOICES]
    values = [counts[status_id] for status_id, _ in STATUS_CHOICES]
    colors = [STATUS_COLORS[status_id] for status_id, _ in STATUS_CHOICES]

    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    if sum(values) == 0:
        ax.text(0.5, 0.5, "No reports yet", ha="center", va="center", fontsize=10)
        ax.axis("off")
    else:
        wedges, _texts, _autotexts = ax.pie(
            values,
            colors=colors,
            wedgeprops={"width": 0.42, "edgecolor": "white"},
            startangle=90,
            autopct=lambda pct: f"{round(pct)}%" if pct > 0 else "",
            pctdistance=0.79,
            textprops={"fontsize": 8, "color": "#1C2B25"},
        )
        ax.legend(
            wedges,
            labels,
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=False,
            fontsize=8,
        )
    fig.tight_layout()
    return _fig_to_base64(fig)


def trend_line_chart(reports_queryset):
    dates = [r.created_at.date() for r in reports_queryset]
    if not dates:
        fig, ax = plt.subplots(figsize=(6.4, 3.0))
        ax.text(0.5, 0.5, "No reports yet", ha="center", va="center", fontsize=10)
        ax.axis("off")
        return _fig_to_base64(fig)

    series = pd.Series(dates).value_counts().sort_index()
    cumulative = series.cumsum()

    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.plot(
        cumulative.index,
        cumulative.values,
        color="#A6532D",
        linewidth=2,
        marker="o",
        markersize=3,
    )
    ax.fill_between(cumulative.index, cumulative.values, color="#A6532D", alpha=0.12)
    ax.set_ylabel("Cumulative reports")
    fig.autofmt_xdate(rotation=30)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    fig.tight_layout()
    return _fig_to_base64(fig)
