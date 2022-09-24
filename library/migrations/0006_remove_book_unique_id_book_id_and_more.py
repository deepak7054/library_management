# Generated by Django 4.1.1 on 2022-09-24 05:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_remove_book_is_borrowed_bookissue_is_returned_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='unique_id',
        ),
        migrations.AddField(
            model_name='book',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 24, 5, 48, 14, 970319), help_text='Book Due date'),
        ),
    ]