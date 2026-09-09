from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("room_booking", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="occupancy",
            new_name="Occupancy",
        ),
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
                condition=models.Q(end_date__gt=models.F("start_date")),
                name="occupancy_end_after_start",
            ),
        ),
        migrations.AddIndex(
            model_name="occupancy",
            index=models.Index(fields=["room", "start_date", "end_date"], name="room_bookin_room_id_8e4f6c_idx"),
        ),
        migrations.AddIndex(
            model_name="occupancy",
            index=models.Index(fields=["user", "start_date"], name="room_bookin_user_id_3c8a34_idx"),
        ),
    ]
