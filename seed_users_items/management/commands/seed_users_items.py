# # from django.core.management.base import BaseCommand
# # from auctions.models import User, Listing, Category, Comment

# # class Command(BaseCommand):
# #     def handle(self, *args, **options):
# #         default_category, created = Category.objects.get_or_create(name='Default Category')
# #         # Create users
# #         users = [
# #             {'username': 'adminbro', 'password': '1234'},
# #             {'username': 'trnbro', 'password': '1234'},
# #             {'username': 'bobrock', 'password': '1234'},
# #             {'username': 'siroliver', 'password': '1234'},
# #         ]        
# #         for user in users:
# #             user = User.objects.create_user(**user)

# #             listings = [
# #                 {'user': user, 'title': 'Beautiful NFT', 'text': 'Very unique, beautiful NFT.', 'start_bid': 10.00, 'category': default_category},
# #                 {'user': user, 'title': 'Basketball ball', 'text': 'Handmade basketball ball.', 'start_bid': 20.00, 'category': default_category},
# #                 {'user': user, 'title': 'Stylish hat', 'text': 'Hat that fits on most heads.', 'start_bid': 25.00, 'category': default_category},
# #                 {'user': user, 'title': 'Golden watch', 'text': 'If you wont, Bing will buy it.', 'start_bid': 49.00, 'category': default_category},
# #             ]
# #             for listing in listings:
# #                 listing = Listing.objects.create(**listings)
# #                 for i in range(3): 
# #                     Comment.objects.create(user=user, listing=listing, text=f'Thats a nice item for my collection. {i + 1}')

# from django.core.management.base import BaseCommand
# from auctions.models import User, Listing, Category, Comment

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         default_category, created = Category.objects.get_or_create(name='Default Category')
#         # Create users
#         users = [
#             {'username': 'adminbro', 'password': '1234'},
#             {'username': 'trnbro', 'password': '1234'},
#             {'username': 'bobrock', 'password': '1234'},
#             {'username': 'siroliver', 'password': '1234'},
#         ]        
#         for user_data in users:
#             user = User.objects.create_user(**user_data)

#             listings = [
#                 {'user': user, 'title': 'Beautiful NFT', 'text': 'Very unique, beautiful NFT.', 'start_bid': 10.00, 'category': default_category},
#                 {'user': user, 'title': 'Basketball ball', 'text': 'Handmade basketball ball.', 'start_bid': 20.00, 'category': default_category},
#                 {'user': user, 'title': 'Stylish hat', 'text': 'Hat that fits on most heads.', 'start_bid': 25.00, 'category': default_category},
#                 {'user': user, 'title': 'Golden watch', 'text': 'If you wont, Bing will buy it.', 'start_bid': 49.00, 'category': default_category},
#             ]
#             for listing_data in listings:
#                 listing = Listing.objects.create(**listing_data)
#                 for i in range(3): 
#                     Comment.objects.create(user=user, listing=listing, text=f'Thats a nice item for my collection. {i + 1}')

from django.core.management.base import BaseCommand
from auctions.models import User, Listing, Category, Comment

class Command(BaseCommand):
    def handle(self, *args, **options):
        default_category, created = Category.objects.get_or_create(name='Default Category')
        # Create users
        users = [
            {'username': 'adminbro', 'password': '1234'},
            {'username': 'trnbro', 'password': '1234'},
            {'username': 'bobrock', 'password': '1234'},
            {'username': 'siroliver', 'password': '1234'},
        ]        
        listings = [
            {'title': 'Beautiful NFT', 'text': 'Very unique, beautiful NFT.', 'start_bid': 10.00, 'category': default_category},
            {'title': 'Basketball ball', 'text': 'Handmade basketball ball.', 'start_bid': 20.00, 'category': default_category},
            {'title': 'Stylish hat', 'text': 'Hat that fits on most heads.', 'start_bid': 25.00, 'category': default_category},
            {'title': 'Golden watch', 'text': 'If you wont, Bing will buy it.', 'start_bid': 49.00, 'category': default_category},
        ]
        for user_data, listing_data in zip(users, listings):
            user = User.objects.create_user(**user_data)
            listing_data['user'] = user
            listing = Listing.objects.create(**listing_data)
            for i in range(3): 
                Comment.objects.create(user=user, listing=listing, text=f'Thats a nice item for my collection. {i + 1}')
