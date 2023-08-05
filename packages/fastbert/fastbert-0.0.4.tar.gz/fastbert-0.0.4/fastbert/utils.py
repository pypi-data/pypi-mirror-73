# coding: utf-8
"""
Some utils for fastbert.

@author: Weijie Liu
"""
import os
import json
import torch
import random
import numpy as np
from argparse import Namespace
import urllib


def hello():
    print("Hello FastBERT!")


def load_hyperparam(config_path,
                    file_dir=None,
                    args=None):
    with open(config_path, "r", encoding="utf-8") as f:
        param = json.load(f)
        for key, value in param.items():
            if isinstance(key, str) and key.endswith('_path'):
                param[key] = os.path.join(file_dir, value)

    if args is None:
        args_dict = {}
    else:
        args_dict = vars(args)
    args_dict.update(param)
    
    args = Namespace(**args_dict)
    return args


def check_or_download(file_path,
                      file_url,
                      file_url_bak=None,
                      verbose=True):
    if os.path.exists(file_path):
        return True
    else:
        if verbose:
            print("{} are not exist.".format(file_path))
            print("Download the model file from {}".format(file_url))
        try:
            urllib.request.urlretrieve(file_url, file_path)
            print("Download the model file successfully.")
        except Exception as error:
            infos = "\n[Error]: Download model file failed!"
            options = \
                "[Option]: You can download model file from [URL_A] or [URL_B], " + \
                "and save it as [PATH] by yourself. \n" + \
                "URL_A: {}\nURL_B:{}\nPATH: {} ". \
                format(file_url, file_url_bak, file_path)
            raise Exception(infos + '\n' + options)


def calc_uncertainty(p,
                     labels_num):
    entropy = torch.distributions.Categorical(probs=p).entropy()
    normal = -np.log(1.0/labels_num)
    return entropy / normal


def shuffle_pairs(list_a,
                  list_b):
    randnum = random.randint(0, 100)
    random.seed(randnum)
    random.shuffle(list_a)
    random.seed(randnum)
    random.shuffle(list_b)
    return list_a, list_b
