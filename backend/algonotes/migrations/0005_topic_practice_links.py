from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("algonotes", "0004_topic_template_modes"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="practice_links",
            field=models.JSONField(blank=True, default=dict, verbose_name="题目链接"),
        ),
    ]
