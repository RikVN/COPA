# Overview

This repo contains experiments in the [MaCoCu](https://macocu.eu/) project for fine-tuning LMs on the [COPA](https://www.researchgate.net/publication/221251392_Choice_of_Plausible_Alternatives_An_Evaluation_of_Commonsense_Causal_Reasoning) data set (choosing plausible alternatives).

Each example contains a premise and two possible follow-up sentences. The model has to choose the ones which is the most plausible.

We had the original English data set human-translated to Bulgarian, Macedonian and Turkish and will perform experiments on those languages.

## Setting up

Clone the repo:

```
git clone https://github.com/RikVN/COPA
cd COPA
```

Setup a Conda environment:

```
conda create -n copa python=3.8
conda activate copa
```

Install transformers from source to avoid errors:

```
git clone https://github.com/huggingface/transformers
cd transformers
pip install -e .
cd ../
```

Install our own requirements:

```
pip install -r requirements.txt
```

## Data

The data is available in the ``data/`` folder. We will first convert it to a JSON, so ``src/run_copa.py`` is able to work with it.

The script has multiple options to put the data in different formats by adding -d:

* -d all   : just keep all available data
* -d token : add a token that indicates whether the example is "cause" or "effect"
* -d cause : only keep the "cause" data
* -d effect: only keep the "effect" data

When using ``-d token``, you have to specify the iso language code (bg, mk, tr) with -l.

For example, if you only want to add a token to the Bulgarian test set, run this:

```
python src/copa_to_json.py -i data/bg.copa.test -o data/bg.copa.test.token.json -d token -l bg
```

However, in our experiments, it was preferable to just keep all the data. Simply run this to apply this to all data sets:

```
./src/preprocess.sh
```

## Experiments

Each experiments takes in a configuration file as **only** argument. You need to specify the data sets and LM in this file. For example, the Turkish MaCoCu model config is specified in ``config/tr_xlmr_macocu.json``. We have added the config files for all our experiments.

Running an experiment is as simple as:

```
python src/run_copa.py config/tr_xlmr_macocu.json
```

We use the AutoModelForMultipleChoice to do the classification. This should work out of the box for most models.

By default, this will average over **10 runs**, since the data set is so small. You can edit this in the `run_copa.py`` script. Average accuracies and standard deviations are printed after training.

Since training is fast, we never save any of the trained models for storage reasons. You can easily change this is in the config settings, though.
