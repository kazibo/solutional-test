import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from mainapp.models import Product, Order, OrderProduct


@api_view(['GET'])
def products_view(request):
    products = Product.objects.all().values("id", "name", "price")
    return Response(products)


@api_view(['POST'])
def orders_view(request):
    order = Order()
    order.save()
    return Response(serialize_orders([order])[0], status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH'])
def orders_single_view(request, order_id):
    if request.method == "GET":
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_orders([order])[0])

    if request.method == "PATCH":
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        request_body = json.loads(request.body)
        if "status" in request_body:
            if request_body["status"] == "PAID":
                order.status = "PAID"
                order.save()
                return Response("OK")
        return Response("Invalid order status", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def order_products_view(request, order_id):
    if request.method == "GET":
        return Response(get_order_products(order_id))

    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        if order.status == "PAID":
            return Response("Invalid parameters", status=status.HTTP_400_BAD_REQUEST)
        request_body = json.loads(request.body)
        try:
            for product_id in request_body:
                try:
                    order_product = OrderProduct.objects.get(order=order_id, product=product_id)
                    order_product.quantity = order_product.quantity + 1
                    order_product.save()
                except OrderProduct.DoesNotExist:
                    OrderProduct(order=Order(id=order_id), product=Product(
                        id=product_id)).save()  # not effective, but bulk actions caused id conflicts
        except ValueError:
            return Response("Invalid parameters", status=status.HTTP_400_BAD_REQUEST)
        return Response("OK", status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def order_products_single_view(request, order_id, order_product_id):
    if request.method == "PATCH":
        try:
            order_product = OrderProduct.objects.get(order=order_id, id=order_product_id, is_replacement=False)
        except OrderProduct.DoesNotExist:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        try:
            request_body = json.loads(request.body)
            if "quantity" in request_body:
                order_product.quantity = request_body["quantity"]
                order_product.save()
                return Response("OK")
            if "replaced_with" in request_body:
                try:
                    order = Order.objects.get(id=order_id)
                except Order.DoesNotExist:
                    return Response("Invalid parameters", status=status.HTTP_400_BAD_REQUEST)
                try:
                    product = Product.objects.get(id=request_body["replaced_with"]["product_id"])
                except Product.DoesNotExist:
                    return Response("Invalid parameters", status=status.HTTP_400_BAD_REQUEST)
                if order.status == "PAID":
                    if order_product.replaced_with:
                        OrderProduct.objects.get(id=order_product.replaced_with.id).delete()
                    replacement = OrderProduct(order=order, product=product,
                                               quantity=request_body["replaced_with"]["quantity"], is_replacement=True)
                    order_product.replaced_with = replacement
                    replacement.save()
                    order_product.save()
                    return Response("OK")
                return Response("Invalid parameters", status=status.HTTP_400_BAD_REQUEST)
            return Response("Invalid parameters", status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response("Invalid parameters", status=status.HTTP_400_BAD_REQUEST)
        return Response("OK")


def serialize_orders(order_query):
    result = []
    for order in order_query:
        order_products_paid_query = OrderProduct.objects.filter(order=order.id, is_replacement=False)
        billed = sum([orderProduct.product.price * orderProduct.quantity for orderProduct in order_products_paid_query])
        order_products_sent_query = OrderProduct.objects.filter(order=order.id, replaced_with=None)
        total = sum([orderProduct.product.price * orderProduct.quantity for orderProduct in order_products_sent_query])
        discount = max(total - billed, 0)
        returns = max(billed - total, 0)
        paid = billed if order.status == "PAID" else 0
        result.append(
            {"amount": {"discount": discount, "paid": paid, "returns": returns, "total": total}, "id": order.id,
             "products": get_order_products(order.id), "status": order.status})
    return result


def get_order_products(order_id):
    order_products_query = OrderProduct.objects.filter(order=order_id, is_replacement=False)
    result = []
    for order_product in order_products_query:
        result.append(serialize_order_product(order_product))
    return result


def serialize_order_product(order_product):
    if not order_product:
        return None
    replacement = None
    if order_product.replaced_with:
        replacement = OrderProduct.objects.get(id=order_product.replaced_with.id)
    return {"id": order_product.id, "name": order_product.product.name, "price": order_product.product.price,
            "product_id": order_product.product.id, "quantity": order_product.quantity,
            "replaced_with": serialize_order_product(replacement)}
