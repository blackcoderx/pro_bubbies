# Generated by Django 5.0.2 on 2024-04-15 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0003_alter_room_options_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]