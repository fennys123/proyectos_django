# Generated by Django 4.2.9 on 2024-01-24 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cat', models.CharField(max_length=150)),
                ('desc', models.TextField(help_text='Descripción corta de la categoría')),
            ],
        ),
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('estreno', models.IntegerField(default=2000)),
                ('imagen', models.URLField(help_text='De imdb mismo')),
                ('resumen', models.TextField(help_text='Descripción corta')),
                ('favoritos', models.IntegerField(default=0)),
                ('fecha_created', models.DateTimeField(auto_now_add=True)),
                ('fecha_updated', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cine.categoria')),
            ],
            options={
                'ordering': ['titulo'],
            },
        ),
    ]
