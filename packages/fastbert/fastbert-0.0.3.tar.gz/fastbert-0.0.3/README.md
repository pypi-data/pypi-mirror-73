# FastBERT_pypi

The pypi version of [FastBERT](https://github.com/autoliuweijie/FastBERT).


## Install

Install ``fastbert`` with ``pip``.
```sh
$ pip install fastbert
```

## Usage

Currently the project only supports single sentence classification, we will add other functions one after another.

```python
from fastbert import FastBERT

# Loading your dataset
labels = ['T', 'F']
sents_train = [
    'I am a bad guy!',
    'I am a good guy!',
    ...
]
labels_train = [
    'T',
    'F',
    ...
]

# Create and training model
model = FastBERT("google_bert_base_zh", labels=labels, device='cuda:0')
model.fit(
    sents_train,
    labels_train,
    model_saving_path='./fastbert.bin',
)

# Loading model and make inference
model.load_model('./fastbert.bin')
label = model('I am a normal guy!', speed=0.7)
```
