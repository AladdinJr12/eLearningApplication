# Generated by Django 4.2.17 on 2025-03-05 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning_application', '0005_alter_chatmessages_receiverid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessages',
            name='receiverID',
        ),
        migrations.RemoveField(
            model_name='chatmessages',
            name='senderID',
        ),
        migrations.DeleteModel(
            name='ChatGroup',
        ),
        migrations.DeleteModel(
            name='ChatMessages',
        ),
    ]
