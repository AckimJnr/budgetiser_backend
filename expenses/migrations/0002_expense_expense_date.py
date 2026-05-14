# Generated manually for expense_date

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="expense_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
