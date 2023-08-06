# ModelEngine

The ModelEngine repo is used to integrate new Tensorflow models into the OsmosisAI platform, though it is not strictly related to that platform. The main feature of this codebase is its simplified API for training and inferencing with common models. Currently support is only available for YOLOv3 models, with support for more models being planned.  

## Installation

To use ModelEngine, install using pip:

`pip install model-engine`

## Usage

```python
from model_engine.models import get_model

yolo_model = get_model('yolov3:object_detection')

# Note that as of this version, utilities for creating records in the right format 
# are not ported to this project but are coming soon.
record_provider = yolo_model.Meta.record_provider('train.tfrecord', 'val.tfrecord', 'label_map.txt')

model_instance = yolo_model()  
model_instance.train(record_provider)
```

This API is in flux at the moment and derives some design principles from other projects such as Django. The current design is mainly influenced by decisions we've made in the past for our core OsmosisAI platform. Changing some things here requires making sure our platform is also ready for the change to be made, but we are open to making changes as necessary to support the wide usage of ModelEngine.

## Models

Currently we support the following models:
* YOLOv3

Support for more models is being planned and will be updated here later.

## Goals

The API of this project is still in flux due to limited model availability, but we plan to try and keep it as simple and flexible as possible. One of our main goals is to reduce the amount of complexity around using model code inside other codebases. We will import other projects where possible to reduce the amount of code needing management, but many Tensorflow 2 codebases rely heavily on the usage of Abseil for configuration which does not play nicely when integrating with other code.

We also strive to keep outside dependencies to a minimum and currently aim to only require the necessary packages for Tensorflow 2.2.0.

## Contributing

Contributions are welcome from anyone. Contributions here will also make the open-source OsmosisAI platform better by adding support for training and inferencing with new models.

If bugs or other issues are found please submit an issue using GitHub or if preferred our corporate email: [contact@osmosisai.com](mailto:contact@osmosisai.com).

To see a list of sources we've used take a look at the [acknowledgements](ACKNOWLEDGEMENTS.md).
