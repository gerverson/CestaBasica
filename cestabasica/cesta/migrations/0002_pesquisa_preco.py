# Generated by Django 2.1.7 on 2019-02-15 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cesta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pesquisa_preco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=6, max_digits=8)),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.estabelecimento')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.eventos')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cesta.produto')),
            ],
        ),
    ]
