# Generated by Django 3.2.7 on 2021-09-16 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='NEW', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('is_replacement', models.BooleanField(default=False)),
                ('order', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
                ('replaced_with', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.orderproduct')),
            ],
            options={
                'unique_together': {('order', 'product', 'replaced_with')},
            },
        ),
    ]
