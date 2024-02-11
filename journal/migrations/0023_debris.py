# Generated by Django 4.2.9 on 2024-02-04 22:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0019_task"),
        ("catalog", "0011_alter_externalresource_id_type_and_more"),
        ("journal", "0022_letterboxdimporter"),
    ]

    operations = [
        migrations.CreateModel(
            name="Debris",
            fields=[
                (
                    "piece_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="journal.piece",
                    ),
                ),
                ("visibility", models.PositiveSmallIntegerField(default=0)),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("edited_time", models.DateTimeField(auto_now=True)),
                ("metadata", models.JSONField(default=dict)),
                (
                    "remote_id",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                ("class_name", models.CharField(max_length=50)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="catalog.item"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="users.apidentity",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("journal.piece",),
        ),
    ]