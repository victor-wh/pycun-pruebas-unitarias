def calculate_taxes_per_item(quantity, price, tax_percentage):
    """
    :param quantity:
    :param price:
    :param tax_percentage:
    """
    sub_total_article = quantity * price
    price_after_taxes = (1 + (tax_percentage / 100)) * sub_total_article
    total_tax = price_after_taxes - sub_total_article

    return {
        "sub_total": sub_total_article,
        "total_tax": total_tax,
        "total_before_tax": sub_total_article,
        "total_after_taxes": price_after_taxes,
    }
