from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("algonotes", "0002_topic_exam_years"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="template_codes",
            field=models.JSONField(blank=True, default=dict, verbose_name="多语言模板代码"),
        ),
    ]

