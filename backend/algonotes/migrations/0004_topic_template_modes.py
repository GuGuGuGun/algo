from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("algonotes", "0003_topic_template_codes"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="template_modes",
            field=models.JSONField(blank=True, default=dict, verbose_name="模板模式代码"),
        ),
    ]
