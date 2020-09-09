# Generated by Django 2.2.10 on 2020-09-06 12:54

import covidUsers.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, max_length=100)),
                ('latitude', models.FloatField(blank=True, default=0.0)),
                ('longitude', models.FloatField(blank=True, default=0.0)),
                ('age', models.IntegerField(default=0.0)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=2, null=True)),
                ('otpVerified', models.BooleanField(blank=True, default=False, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', covidUsers.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.CharField(max_length=250)),
                ('lang', models.CharField(blank=True, choices=[('E', 'English'), ('M', 'Marathi')], max_length=2, null=True)),
                ('isChecked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CoronaHospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospitalImage', models.ImageField(blank=True, null=True, upload_to='media/uploads/', verbose_name='Hospital Image')),
                ('hospitalName', models.CharField(blank=True, max_length=255, null=True, verbose_name='Hospital Name')),
                ('hospitalAddress', models.TextField(verbose_name='Hospital Address')),
                ('directions', models.CharField(blank=True, max_length=100, null=True, verbose_name='Directions')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Corona Hospitals',
            },
        ),
        migrations.CreateModel(
            name='CovidInitialQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, null=True)),
                ('lang', models.CharField(blank=True, choices=[('E', 'English'), ('M', 'Marathi')], max_length=2, null=True)),
                ('orderNumber', models.IntegerField(blank=True, default=0, null=True)),
                ('isMultipleChoice', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('choices', models.ManyToManyField(to='covidUsers.Choice')),
            ],
        ),
        migrations.CreateModel(
            name='DropdownValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=250, null=True)),
                ('lang', models.CharField(blank=True, choices=[('E', 'English'), ('M', 'Marathi')], max_length=2, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='Url')),
            ],
            options={
                'verbose_name_plural': 'Urls',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True, verbose_name='Tilte')),
                ('question', models.TextField(blank=True, null=True, verbose_name='Message')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Message Center',
            },
        ),
        migrations.CreateModel(
            name='NewsFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/uploads/', verbose_name='Feed Image')),
                ('video', models.FileField(blank=True, null=True, upload_to='media/uploads/', verbose_name='Feed Video')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tilte')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='Link')),
                ('lang', models.CharField(blank=True, choices=[('E', 'English'), ('M', 'Marathi')], max_length=2, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'News Feeds',
            },
        ),
        migrations.CreateModel(
            name='QuarantineSymptomsChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=250)),
                ('lang', models.CharField(blank=True, choices=[('E', 'English'), ('M', 'Marathi')], max_length=2, null=True)),
                ('isChecked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuarantineSymptomsQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom', models.TextField(blank=True, null=True)),
                ('lang', models.CharField(blank=True, choices=[('E', 'English'), ('M', 'Marathi')], max_length=2, null=True)),
                ('orderNumber', models.IntegerField(blank=True, default=0, null=True)),
                ('finalAnswer', models.CharField(blank=True, max_length=100, null=True, verbose_name='finalAnswer')),
                ('isMultipleChoice', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('choices', models.ManyToManyField(to='covidUsers.QuarantineSymptomsChoices')),
            ],
        ),
        migrations.CreateModel(
            name='QurantineSymtomsAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covidUsers.QuarantineSymptomsChoices')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covidUsers.QuarantineSymptomsQuestions')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, choices=[('D', 'Doctor'), ('C', 'Counsellor'), ('P', 'patient'), ('O', 'Others')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserQuarantineSymptomsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onDate', models.DateTimeField(blank=True, null=True)),
                ('result', models.CharField(blank=True, max_length=100, null=True, verbose_name='result')),
                ('data', models.ManyToManyField(blank=True, null=True, to='covidUsers.QurantineSymtomsAnswers')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFireBaseDeviceToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_token', models.CharField(default='', max_length=255)),
                ('device_type', models.CharField(default='', max_length=255)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CovidInitialQuestionsResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covidUsers.Choice')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covidUsers.CovidInitialQuestions')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='lang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='covidUsers.DropdownValues'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_role',
            field=models.ManyToManyField(to='covidUsers.Role', verbose_name='user_role'),
        ),
    ]
