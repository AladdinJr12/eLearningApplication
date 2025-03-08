# Generated by Django 4.2.17 on 2025-02-27 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.TextField(choices=[('Teacher', 'Teacher'), ('Student', 'Student')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseID', models.AutoField(primary_key=True, serialize=False)),
                ('courseTitle', models.TextField(max_length=256)),
                ('courseDescription', models.TextField(max_length=256)),
                ('courseCreatedDate', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('lessonID', models.AutoField(primary_key=True, serialize=False)),
                ('video_link', models.URLField(blank=True, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='e_learning_application.course')),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('teacherID', models.AutoField(primary_key=True, serialize=False)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('studentID', models.AutoField(primary_key=True, serialize=False)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='StatusUpdates',
            fields=[
                ('statusUpdatesId', models.AutoField(primary_key=True, serialize=False)),
                ('status_content', models.TextField(max_length=256)),
                ('status_update_date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.appuser')),
            ],
        ),
        migrations.CreateModel(
            name='McqQuestion',
            fields=[
                ('questionID', models.AutoField(primary_key=True, serialize=False)),
                ('question_content', models.TextField(max_length=256)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='e_learning_application.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedbackID', models.AutoField(primary_key=True, serialize=False)),
                ('feedbackText', models.TextField(max_length=256)),
                ('date_of_feedback', models.DateField(auto_now_add=True)),
                ('courseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.course')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.students')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollments',
            fields=[
                ('enrollmentID', models.AutoField(primary_key=True, serialize=False)),
                ('enrollment_date', models.DateField(auto_now_add=True)),
                ('courseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.course')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.students')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='teacherID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_learning_application.teachers'),
        ),
        migrations.CreateModel(
            name='ChatMessages',
            fields=[
                ('ChatMessageID', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField(max_length=256)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('receiverID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='e_learning_application.teachers')),
                ('senderID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='e_learning_application.students')),
            ],
        ),
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('chatGroupID', models.AutoField(primary_key=True, serialize=False)),
                ('ChatGroup_creation_date', models.DateField(auto_now_add=True)),
                ('name', models.TextField(max_length=256)),
                ('courseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_learning_application.course')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answerID', models.AutoField(primary_key=True, serialize=False)),
                ('answer_text', models.TextField(max_length=256)),
                ('is_correct', models.BooleanField(default=False)),
                ('related_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='e_learning_application.mcqquestion')),
            ],
        ),
        migrations.AddConstraint(
            model_name='enrollments',
            constraint=models.UniqueConstraint(fields=('studentID', 'courseID'), name='unique_student_course'),
        ),
    ]
