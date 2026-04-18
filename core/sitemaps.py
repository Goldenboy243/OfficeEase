from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from courses.models import Course


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "about_us", "how_it_works", "word_course", "excel_course", "powerpoint_course"]

    def location(self, item):
        return reverse(item)


class StructuredCourseSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Course.objects.all()

    def location(self, obj):
        return reverse("structured_course", args=[obj.id])
