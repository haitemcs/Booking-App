from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("room_booking", "0002_fix_occupancy_and_booking_constraints"),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "CREATE UNIQUE INDEX auth_user_email_unique_nonempty "
                "ON auth_user (LOWER(email)) WHERE email <> '';"
            ),
            reverse_sql="DROP INDEX auth_user_email_unique_nonempty;",
        ),
    ]
