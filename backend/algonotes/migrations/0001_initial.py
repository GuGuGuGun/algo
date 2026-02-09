from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chapter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100, unique=True)),
                ("summary", models.TextField()),
                ("order", models.PositiveIntegerField(default=1)),
                (
                    "difficulty",
                    models.CharField(
                        choices=[("easy", "简单"), ("medium", "中等"), ("hard", "困难")],
                        default="medium",
                        max_length=10,
                    ),
                ),
                ("estimated_hours", models.PositiveIntegerField(default=4)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "章节", "verbose_name_plural": "章节", "ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="StudyPlan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("week", models.PositiveIntegerField(unique=True)),
                ("target", models.CharField(max_length=120)),
                ("focus", models.CharField(max_length=200)),
                ("recommended_hours", models.PositiveIntegerField(default=12)),
            ],
            options={"verbose_name": "学习计划", "verbose_name_plural": "学习计划", "ordering": ["week"]},
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("knowledge_point", models.CharField(max_length=180)),
                ("note", models.TextField()),
                ("template_code", models.TextField(blank=True)),
                ("exam_tip", models.TextField(blank=True)),
                ("is_key_for_exam", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "chapter",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="topics", to="algonotes.chapter"),
                ),
            ],
            options={"verbose_name": "知识点", "verbose_name_plural": "知识点", "ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="ProblemTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, unique=True)),
                (
                    "category",
                    models.CharField(
                        choices=[("hot100", "Hot100"), ("exam", "考研常考"), ("template", "模板题")],
                        default="exam",
                        max_length=20,
                    ),
                ),
                ("topics", models.ManyToManyField(blank=True, related_name="tags", to="algonotes.topic")),
            ],
            options={"verbose_name": "题目标签", "verbose_name_plural": "题目标签"},
        ),
    ]

