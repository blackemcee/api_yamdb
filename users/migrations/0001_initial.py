# Generated by Django 3.0.5 on 2021-06-03 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=True, null=True)),
                ('username', models.CharField(blank=True, max_length=200, unique=True, verbose_name='username')),
                ('role', models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=10)),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='description')),
                ('bio', models.CharField(blank=True, max_length=200, null=True, verbose_name='bio')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='last name')),
                ('token', models.CharField(blank=True, max_length=200, null=True, verbose_name='token')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.CheckConstraint(check=models.Q(role__in=['user', 'moderator', 'admin']), name='users_customuser_role_valid'),
        ),
    ]
