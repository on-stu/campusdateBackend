# Generated by Django 3.2.5 on 2022-06-07 06:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=30, unique=True)),
                ('password', models.CharField(blank=True, max_length=255)),
                ('photoUrl', models.FileField(blank=True, upload_to='imgs/%Y/%m/%d/%H/%M/%S')),
                ('nickname', models.CharField(blank=True, max_length=20)),
                ('sex', models.CharField(blank=True, max_length=8)),
                ('birthday', models.DateTimeField(null=True)),
                ('payments', models.JSONField(default=list)),
                ('myHobbies', models.JSONField(default=list)),
                ('myIdeals', models.JSONField(default=list)),
                ('whoAmI', models.JSONField(default=list)),
                ('introduction', models.TextField(blank=True, max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('chatRooms', models.JSONField(default=list)),
                ('university', models.CharField(blank=True, max_length=20)),
                ('accepted', models.JSONField(default=list)),
                ('myHobbiesScore', models.JSONField(default=list)),
                ('myIdealsScore', models.JSONField(default=list)),
                ('whoAmIScore', models.JSONField(default=list)),
                ('private', models.BooleanField(default=False)),
                ('skipUser', models.JSONField(default=list)),
                ('userNotificationToken', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Charm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('content', models.TextField(blank=True, max_length=500)),
                ('authorId', models.IntegerField(blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('comments', models.JSONField(default=list)),
                ('thumbs', models.JSONField(default=list)),
                ('isAnonymous', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creatorId', models.IntegerField(default=0)),
                ('participants', models.JSONField(default=list)),
                ('lastAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('isActive', models.BooleanField(default=True)),
                ('content', models.TextField(blank=True, max_length=500)),
                ('authorId', models.IntegerField(blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('comments', models.JSONField(default=list)),
                ('thumbs', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('done', models.BooleanField(default=False)),
                ('content', models.TextField(blank=True, max_length=500)),
                ('authorId', models.IntegerField(blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('isSecret', models.BooleanField(default=True)),
                ('answers', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('isImportant', models.BooleanField(default=True)),
                ('content', models.TextField(blank=True, max_length=500)),
                ('authorId', models.IntegerField(blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('comments', models.JSONField(default=list)),
                ('thumbs', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('content', models.TextField(blank=True, max_length=500)),
                ('authorId', models.IntegerField(blank=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('comments', models.JSONField(default=list)),
                ('thumbs', models.JSONField(default=list)),
                ('isAnonymous', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senderId', models.CharField(blank=True, max_length=100000)),
                ('receiverId', models.CharField(blank=True, max_length=100000)),
                ('content', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('isRead', models.BooleanField(default=False)),
                ('chatRoomId', models.ForeignKey(db_column='chat_room_id', on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='api.chatroom')),
            ],
        ),
    ]
