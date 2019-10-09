# Generated by Django 2.1.7 on 2019-03-25 19:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='cidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='estabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('endereco', models.CharField(max_length=100)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.cidade')),
            ],
        ),
        migrations.CreateModel(
            name='estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('sigla', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.IntegerField(default=2)),
                ('ano', models.PositiveIntegerField(help_text='Use the following format: <YYYY>', validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2019)])),
            ],
        ),
        migrations.CreateModel(
            name='marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='pesquisa_preco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.estabelecimento')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.evento')),
            ],
        ),
        migrations.CreateModel(
            name='produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('codbarras', models.CharField(max_length=20)),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=8)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.marca')),
            ],
        ),
        migrations.CreateModel(
            name='tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cestabasica', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='unidadeMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.tipo'),
        ),
        migrations.AddField(
            model_name='produto',
            name='unidadeMedida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.unidadeMedida'),
        ),
        migrations.AddField(
            model_name='pesquisa_preco',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.produto'),
        ),
        migrations.AddField(
            model_name='cidade',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.estado'),
        ),
    ]
