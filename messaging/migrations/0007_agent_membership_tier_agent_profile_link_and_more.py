# Generated by Django 5.1.3 on 2024-11-06 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0006_alter_agent_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='membership_tier',
            field=models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium'), ('VIP', 'VIP')], default='standard', max_length=10),
        ),
        migrations.AddField(
            model_name='agent',
            name='profile_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='account_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='loan_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
