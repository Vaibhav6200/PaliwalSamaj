from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SamajApp', '0030_deduplicate_state_city_village'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='state_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
