# Generated by Django 4.0.1 on 2022-01-17 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0005_tweet_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tweets.tweet'),
        ),
    ]
