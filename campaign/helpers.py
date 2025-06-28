from clients.models import Product
from campaign.models import Message

def get_company_products(company):
    subscribed_company= company
    products = Product.objects.filter(subscribed_company=subscribed_company)

    return products


def get_messages_and_products(request):
    subscribed_company= request.user.subscribed_company
    products = get_company_products(subscribed_company)
    messages = Message.objects.filter(product__in=products)
    return messages, products