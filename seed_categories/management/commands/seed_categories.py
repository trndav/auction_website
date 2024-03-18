from django.core.management.base import BaseCommand
from auctions.models import Category

class Command(BaseCommand):
    def handle(self, *args, **options):
        default_categories = [
            {'name': 'NFT', 'description': 'NFT items'},
            {'name': 'Clothings', 'description': 'Clothing items'},
            {'name': 'Sport', 'description': 'Sport items'},
            {'name': 'Default Category', 'description': 'Default Category'},
            # Add more default categories as needed
        ]
        for category_data in default_categories:
            Category.objects.create(**category_data)