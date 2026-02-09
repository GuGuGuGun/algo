from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("algonotes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="exam_years",
            field=models.JSONField(blank=True, default=list, verbose_name="408真题年份"),
        ),
    ]

