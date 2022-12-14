# Generated by Django 4.1.1 on 2022-09-28 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_category_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('M', 'Male.'), ('F', 'Female.'), ('PNS', 'Prefer not to say.')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='password1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='password2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='VendorProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=200)),
                ('lname', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=100)),
                ('comp_name', models.CharField(max_length=200)),
                ('comp_reg_no', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.city')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.service')),
            ],
        ),
    ]
