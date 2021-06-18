from mongoengine import Document, IntField, StringField, FloatField

# the stocks schema for the database
class stocks(Document):
    symbol = StringField(required=True, unique=True)
    date = StringField(required=True)
    opening = FloatField(required=True)
    closing = FloatField(required=True)
    difference = FloatField(required=True)