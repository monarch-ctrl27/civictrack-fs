from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from issues.models import Report, random_point_in_district

DEMO_REPORTS = [
    {
        "title": "Deep pothole on Church Street",
        "category": "roads",
        "district": "mangaung",
        "description": "Large pothole near the taxi rank has grown after the recent "
        "rain — two cars have already blown tyres here.",
        "status": "in_progress",
        "date": "2026-09-02",
        "votes": 34,
    },
    {
        "title": "Burst water pipe flooding Hospitaal Street",
        "category": "water",
        "district": "mangaung",
        "description": "Water has been running down the road for four days, and "
        "pressure in nearby homes has dropped badly.",
        "status": "reported",
        "date": "2026-09-14",
        "votes": 51,
    },
    {
        "title": "Transformer down in Zamdela",
        "category": "electricity",
        "district": "feziledabi",
        "description": "No power in the whole block since Friday night. Several "
        "elderly residents are affected.",
        "status": "under_review",
        "date": "2026-09-10",
        "votes": 42,
    },
    {
        "title": "Illegal dumping site growing behind the clinic",
        "category": "dumping",
        "district": "lejweleputswa",
        "description": "Building rubble and household waste keep being dumped on "
        "the open field, attracting rats.",
        "status": "reported",
        "date": "2026-09-17",
        "votes": 19,
    },
    {
        "title": "Streetlights out along the N5 turnoff",
        "category": "electricity",
        "district": "thabomofutsanyana",
        "description": "Three streetlights have been dark for weeks, making the "
        "turnoff unsafe for pedestrians at night.",
        "status": "under_review",
        "date": "2026-09-08",
        "votes": 27,
    },
    {
        "title": "Reported mugging hotspot near the taxi rank",
        "category": "safety",
        "district": "lejweleputswa",
        "description": "Multiple residents report being followed and robbed "
        "walking home after dark near the rank.",
        "status": "reported",
        "date": "2026-09-19",
        "votes": 38,
    },
    {
        "title": "Sewage overflow near the primary school",
        "category": "water",
        "district": "thabomofutsanyana",
        "description": "Raw sewage has been pooling next to the school gate — a "
        "health risk for the learners.",
        "status": "in_progress",
        "date": "2026-09-05",
        "votes": 46,
    },
    {
        "title": "Community hall roof collapsing",
        "category": "infra",
        "district": "xhariep",
        "description": "Part of the community hall ceiling came down during the "
        "last storm and has not been repaired.",
        "status": "reported",
        "date": "2026-09-13",
        "votes": 15,
    },
    {
        "title": "Gravel road washed away after storm",
        "category": "roads",
        "district": "xhariep",
        "description": "Farmers and school transport can no longer safely use the "
        "access road after the recent floods.",
        "status": "resolved",
        "date": "2026-08-28",
        "votes": 22,
    },
    {
        "title": "Illegal dumping along the river bank",
        "category": "dumping",
        "district": "feziledabi",
        "description": "Waste is being tipped directly into the river, affecting "
        "water quality downstream.",
        "status": "resolved",
        "date": "2026-08-22",
        "votes": 29,
    },
    {
        "title": "Persistent water outage in Ward 12",
        "category": "water",
        "district": "lejweleputswa",
        "description": "Taps have been dry on and off for two weeks with no "
        "communication from the municipality.",
        "status": "under_review",
        "date": "2026-09-16",
        "votes": 33,
    },
    {
        "title": "Damaged playground equipment left unsafe",
        "category": "infra",
        "district": "mangaung",
        "description": "Broken swings and exposed metal edges at the park pose an "
        "injury risk to children.",
        "status": "reported",
        "date": "2026-09-18",
        "votes": 12,
    },
]


class Command(BaseCommand):
    help = "Load realistic sample reports across the Free State for demos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing reports before loading demo data.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            deleted, _ = Report.objects.all().delete()
            self.stdout.write(f"Removed {deleted} existing report(s).")

        created = 0
        for item in DEMO_REPORTS:
            if Report.objects.filter(title=item["title"]).exists():
                continue
            x, y = random_point_in_district(item["district"])
            naive_dt = datetime.strptime(item["date"], "%Y-%m-%d")
            report = Report(
                title=item["title"],
                category=item["category"],
                district=item["district"],
                description=item["description"],
                status=item["status"],
                votes=item["votes"],
                map_x=x,
                map_y=y,
                created_at=make_aware(naive_dt),
            )
            report.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded {created} demo report(s)."))
