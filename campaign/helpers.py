from clients.models import Product

def get_company_products(company):
    subscribed_company= company
    products = Product.objects.filter(subscribed_company=subscribed_company)

    return products