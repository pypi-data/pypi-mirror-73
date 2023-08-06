import uuid

import falcon


class Greeting:

    def on_get(self, req, resp):
        resp.body = 'Hello, World!'
        resp.content_type = falcon.MEDIA_TEXT


class Item:

    def __init__(self, data):
        self._id = str(uuid.uuid4())
        self._data = data

    def marshal(self):
        return {'id': self._id, 'data': self._data}

    @property
    def itemid(self):
        return self._id

    @property
    def reference(self):
        return f'/items/{self._id}'


class Store:

    def __init__(self):
        self._store = {}

    def on_delete(self, req, resp):
        self._store.clear()
        resp.status = falcon.HTTP_NO_CONTENT

    def on_get(self, req, resp):
        resp.media = [item.marshal() for item in self._store.values()]

    def on_post(self, req, resp):
        item = Item(req.media)
        self._store[item.itemid] = item
        resp.location = item.reference
        resp.media = item.marshal()
        resp.status = falcon.HTTP_CREATED

    def on_delete_item(self, req, resp, itemid):
        self._store.pop(itemid, None)
        resp.status = falcon.HTTP_NO_CONTENT

    def on_get_item(self, req, resp, itemid):
        item = self._store.get(itemid)
        if not item:
            raise falcon.HTTPNotFound(
                title='Not Found', description=f'{itemid!r} not in store')
        resp.media = item.marshal()


app = falcon.API()

greeting = Greeting()
store = Store()
app.add_route('/', greeting)
app.add_route('/items', store)
app.add_route('/items/{itemid}', store, suffix='item')
