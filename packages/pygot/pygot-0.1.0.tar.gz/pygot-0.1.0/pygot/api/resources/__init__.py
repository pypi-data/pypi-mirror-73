from .book import Book
from .character import Character
from .house import House


def init_api(api):
    api.add_resource(resource_name="books", resource_class=Book)
    api.add_resource(resource_name="characters", resource_class=Character)
    api.add_resource(resource_name="houses", resource_class=House)
