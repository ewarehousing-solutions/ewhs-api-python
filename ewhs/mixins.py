class ListResourceMixin:
    def list(self, *args, **kwargs):
        return self._api.filter(self.resource, *args, **kwargs)


class DetailResourceMixin:
    def get(self, *args, **kwargs):
        return self._api.get(self.resource, *args, **kwargs)


class CreateResourceMixin:
    def create(self, data, *args, **kwargs):
        return self._api.create(self.resource, data, *args, **kwargs)


class UpdateResourceMixin:
    def update(self, *args, **kwargs):
        return self._api.update(self.resource, *args, **kwargs)


class DeleteResourceMixin:
    def delete(self, *args, **kwargs):
        return self._api.delete(self.resource, *args, **kwargs)
