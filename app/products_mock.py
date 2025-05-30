MOCK_PRODUCTS = {
    "abc123": {
        "id": "abc123",
        "title": "Smartphone Galaxy S21",
        "image": "https://example.com/s21.jpg",
        "price": 2999.99,
        "reviewScore": 4.8
    },
    "tv456": {
        "id": "tv456",
        "title": "Smart TV LG 55” 4K",
        "image": "https://example.com/tv.jpg",
        "price": 3599.90,
        "reviewScore": 4.7
    }
}

def mock_product(product_id: str):
    return MOCK_PRODUCTS.get(product_id)
