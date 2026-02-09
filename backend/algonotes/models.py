from django.db import models


class Chapter(models.Model):
    DIFFICULTY_CHOICES = (
        ("easy", "简单"),
        ("medium", "中等"),
        ("hard", "困难"),
    )

    title = models.CharField(max_length=100, unique=True)
    summary = models.TextField()
    order = models.PositiveIntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    estimated_hours = models.PositiveIntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "章节"
        verbose_name_plural = "章节"

    def __str__(self) -> str:
        return f"{self.order}. {self.title}"


class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=120)
    knowledge_point = models.CharField(max_length=180)
    note = models.TextField()
    template_code = models.TextField(blank=True)
    template_codes = models.JSONField(default=dict, blank=True, verbose_name="多语言模板代码")
    template_modes = models.JSONField(default=dict, blank=True, verbose_name="模板模式代码")
    practice_links = models.JSONField(default=dict, blank=True, verbose_name="题目链接")
    exam_tip = models.TextField(blank=True)
    exam_years = models.JSONField(default=list, blank=True, verbose_name="408真题年份")
    is_key_for_exam = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "知识点"
        verbose_name_plural = "知识点"

    def __str__(self) -> str:
        return self.title


class ProblemTag(models.Model):
    CATEGORY_CHOICES = (
        ("hot100", "Hot100"),
        ("exam", "考研常考"),
        ("template", "模板题"),
    )

    name = models.CharField(max_length=60, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="exam")
    topics = models.ManyToManyField(Topic, related_name="tags", blank=True)

    class Meta:
        verbose_name = "题目标签"
        verbose_name_plural = "题目标签"

    def __str__(self) -> str:
        return self.name


class StudyPlan(models.Model):
    week = models.PositiveIntegerField(unique=True)
    target = models.CharField(max_length=120)
    focus = models.CharField(max_length=200)
    recommended_hours = models.PositiveIntegerField(default=12)

    class Meta:
        ordering = ["week"]
        verbose_name = "学习计划"
        verbose_name_plural = "学习计划"

    def __str__(self) -> str:
        return f"第{self.week}周 - {self.target}"
