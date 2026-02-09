from django.contrib import admin

from .models import Chapter, ProblemTag, StudyPlan, Topic


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "title", "difficulty", "estimated_hours")
    search_fields = ("title", "summary")
    list_filter = ("difficulty",)
    ordering = ("order",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chapter",
        "title",
        "mode_preview",
        "language_preview",
        "practice_link_preview",
        "exam_years_preview",
        "is_key_for_exam",
    )
    list_filter = ("is_key_for_exam", "chapter")
    search_fields = ("title", "knowledge_point")

    @admin.display(description="模板模式")
    def mode_preview(self, obj):
        if not obj.template_modes:
            return "LeetCode"
        labels = {"leetcode": "LeetCode", "nowcoder": "牛客网"}
        return "、".join(labels.get(key, key) for key in obj.template_modes.keys())

    @admin.display(description="代码语言")
    def language_preview(self, obj):
        if not obj.template_codes:
            return "Python"
        labels = {"python": "Python", "cpp": "C/C++", "java": "Java"}
        return "、".join(labels.get(key, key) for key in obj.template_codes.keys())

    @admin.display(description="真题年份")
    def exam_years_preview(self, obj):
        if not obj.exam_years:
            return "-"
        return "、".join(str(year) for year in obj.exam_years)

    @admin.display(description="题链")
    def practice_link_preview(self, obj):
        links = obj.practice_links or {}
        lc_count = len(links.get("leetcode", []))
        nc_count = len(links.get("nowcoder", []))
        return f"LC:{lc_count} / 牛客:{nc_count}"


@admin.register(ProblemTag)
class ProblemTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "week", "target", "focus", "recommended_hours")
    ordering = ("week",)
