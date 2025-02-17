# Generated by Django 5.1.5 on 2025-02-13 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_users_data_nascimento_remove_users_endereco_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turma',
            name='professor',
        ),
        migrations.AddField(
            model_name='turma',
            name='professor',
            field=models.ManyToManyField(blank=True, null=True, related_name='turmas', to='usuarios.professor', verbose_name='Professor'),
        ),
    ]
