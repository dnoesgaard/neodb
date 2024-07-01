# Generated by Django 4.2.13 on 2024-06-29 03:41

import django.db.models.deletion
import django.db.models.functions.text
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mastodon", "0004_alter_mastodonapplication_api_domain_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("mastodon.blueskyaccount", "bluesky account"),
                            ("mastodon.emailaccount", "email account"),
                            ("mastodon.mastodonaccount", "mastodon account"),
                            ("mastodon.threadsaccount", "threads account"),
                        ],
                        db_index=True,
                        max_length=255,
                    ),
                ),
                ("domain", models.CharField(max_length=255)),
                ("uid", models.CharField(max_length=255)),
                ("handle", models.CharField(max_length=1000)),
                ("access_data", models.JSONField(default=dict)),
                ("account_data", models.JSONField(default=dict)),
                ("preference_data", models.JSONField(default=dict)),
                ("followers", models.JSONField(default=list)),
                ("following", models.JSONField(default=list)),
                ("mutes", models.JSONField(default=list)),
                ("blocks", models.JSONField(default=list)),
                ("domain_blocks", models.JSONField(default=list)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("last_refresh", models.DateTimeField(default=None, null=True)),
                ("last_reachable", models.DateTimeField(default=None, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="social_accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BlueskyAccount",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("mastodon.socialaccount",),
        ),
        migrations.CreateModel(
            name="EmailAccount",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("mastodon.socialaccount",),
        ),
        migrations.CreateModel(
            name="MastodonAccount",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("mastodon.socialaccount",),
        ),
        migrations.CreateModel(
            name="ThreadsAccount",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("mastodon.socialaccount",),
        ),
        migrations.AddIndex(
            model_name="socialaccount",
            index=models.Index(
                fields=["type", "handle"], name="index_social_type_handle"
            ),
        ),
        migrations.AddIndex(
            model_name="socialaccount",
            index=models.Index(
                fields=["type", "domain", "uid"], name="index_social_type_domain_uid"
            ),
        ),
        migrations.AddConstraint(
            model_name="socialaccount",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("domain"),
                django.db.models.functions.text.Lower("uid"),
                name="unique_social_domain_uid",
            ),
        ),
        migrations.AddConstraint(
            model_name="socialaccount",
            constraint=models.UniqueConstraint(
                models.F("type"),
                django.db.models.functions.text.Lower("handle"),
                name="unique_social_type_handle",
            ),
        ),
    ]