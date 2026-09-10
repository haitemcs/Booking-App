from django.conf import settings
from django.db import migrations, models
from django.db.models import F, Q
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("room_booking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="occupancy",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="occupancies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="occupancy",
            constraint=models.CheckConstraint(
                condition=Q(end_date__gt=F("start_date")),
                name="occupancy_end_after_start",
            ),
        ),
        migrations.AddIndex(
            model_name="occupancy",
            index=models.Index(fields=["room", "start_date", "end_date"], name="room_bookin_room_id_4d5f5d_idx"),
        ),
        migrations.AddIndex(
            model_name="occupancy",
            index=models.Index(fields=["user", "start_date"], name="room_bookin_user_id_0a1f7b_idx"),
        ),
    ]
