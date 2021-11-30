from .mixins import ListResourceMixin, DeleteResourceMixin, DetailResourceMixin, \
    UpdateResourceMixin, CreateResourceMixin


class Resource(object):
    resource = None

    def __init__(self, api):
        self._api = api


class CRUDResource(
    ListResourceMixin,
    DeleteResourceMixin,
    DetailResourceMixin,
    UpdateResourceMixin,
    CreateResourceMixin,
    Resource):
    pass


class Shipment(ListResourceMixin, DetailResourceMixin, Resource):
    resource = 'shipments'


class Order(ListResourceMixin, DetailResourceMixin, CreateResourceMixin, UpdateResourceMixin, Resource):
    resource = 'orders'
