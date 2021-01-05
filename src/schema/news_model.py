from mongoengine import Document, IntField, StringField, FloatField

class news(Document):
    date = StringField(required=True)
    time = StringField(required=True)
    article = StringField(required=True, unique=True)
    subjectivity = FloatField(required=True)
    polarity = FloatField(required=True)
    company = StringField(required=True, default="")