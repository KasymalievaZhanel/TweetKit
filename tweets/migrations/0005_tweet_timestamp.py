# Generated by Django 4.0.1 on 2022-01-17 00:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_tweetlike_tweet_likes_tweetlike_tweet_tweetlike_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
