from mongoengine import Document, IntField, StringField, FloatField

class stocks(Document):
    symbol = StringField(required=True, unique=True)
    date = StringField(required=True)
    opening = FloatField(required=True)
    closing = FloatField(required=True)