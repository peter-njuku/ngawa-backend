from django.db import migrations
from cloudinary.models import CloudinaryField


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=CloudinaryField(blank=True, null=True, verbose_name='image'),
        ),
    ]
