from django.db import models


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, default="NEW")


class OrderProduct(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # not quite right behaviour, but whatever
    quantity = models.IntegerField(default=1)
    replaced_with = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True)
    is_replacement = models.BooleanField(default=False)

    class Meta:
        unique_together = ('order', 'product', 'replaced_with')
