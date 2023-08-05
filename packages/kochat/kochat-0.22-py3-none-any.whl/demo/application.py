"""
@auther Hyunwoong
@since 7/1/2020
@see https://github.com/gusdnd852
"""
from flask import render_template
from kochat.app import KochatApi
from kochat.data import Dataset
from kochat.loss import CenterLoss, CRFLoss
from kochat.model import intent, embed, entity
from kochat.proc import DistanceClassifier, GensimEmbedder, EntityRecognizer
from demo.scenrios import restaurant, travel, dust, weather

dataset = Dataset(ood=True)
emb = GensimEmbedder(model=embed.FastText())

clf = DistanceClassifier(
    model=intent.CNN(dataset.intent_dict),
    loss=CenterLoss(dataset.intent_dict)
)

rcn = EntityRecognizer(
    model=entity.LSTM(dataset.entity_dict),
    loss=CRFLoss(dataset.entity_dict)
)

kochat = KochatApi(
    dataset=dataset,
    embed_processor=(emb, False),
    intent_classifier=(clf, False),
    entity_recognizer=(rcn, False),
    scenarios=[
        weather, dust, travel, restaurant
    ]
)


@kochat.app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    kochat.app.template_folder = kochat.root_dir + 'templates'
    kochat.app.static_folder = kochat.root_dir + 'static'
    kochat.app.run(port=8080, host='0.0.0.0')
