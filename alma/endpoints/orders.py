from functools import partial

from . import Base
from ..entities import Order
from ..paginated_results import PaginatedResults


class Orders(Base):
    ORDERS_PATH = "/v1/orders"

    def update(self, order_id, data):
        response = self.request(f"{self.ORDERS_PATH}/{order_id}").set_body(data).put()
        return Order(response.json)

    def fetch_all(self, limit: int = 20, starting_after: str = None, **filters):
        args = {"limit": limit}

        if starting_after:
            args["starting_after"] = starting_after

        if filters:
            for attribute, value in filters.items():
                args[attribute] = value

        response = self.request(self.ORDERS_PATH).set_query_params(args).get()

        next_page = partial(self.fetch_all, limit=limit, **filters)
        return PaginatedResults(response.json, Order, next_page)

    def fetch(self, order_id: str = None, limit: int = 20, **filters):
        if order_id is None:
            return self.fetch_all(limit=limit, **filters)
        else:
            response = self.request(f"{self.ORDERS_PATH}/{order_id}").get()
            return Order(response.json)
