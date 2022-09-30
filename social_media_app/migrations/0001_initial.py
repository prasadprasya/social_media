# Generated by Django 3.1.6 on 2022-09-29 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('password', models.TextField(blank=True)),
            ],
            options={
                'db_table': '"users_data"',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, to='social_media_app.users')),
            ],
            options={
                'db_table': '"posts"',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_date', models.DateTimeField(auto_now_add=True)),
                ('liked_by', models.ForeignKey(db_column='liked_by', on_delete=django.db.models.deletion.CASCADE, to='social_media_app.users')),
                ('post_id', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, to='social_media_app.posts')),
            ],
            options={
                'db_table': '"likes"',
            },
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(db_column='follower', on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='social_media_app.users')),
                ('following_to', models.ForeignKey(db_column='following_to', on_delete=django.db.models.deletion.CASCADE, related_name='following_to', to='social_media_app.users')),
            ],
            options={
                'db_table': '"followers"',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('commented_by', models.ForeignKey(db_column='commented_by', on_delete=django.db.models.deletion.CASCADE, to='social_media_app.users')),
                ('post_id', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, to='social_media_app.posts')),
            ],
            options={
                'db_table': '"comments"',
            },
        ),
    ]
