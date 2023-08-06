# Bio Embeddings
The project includes:

- A pipeline that allows to embed a FASTA file choosing from various embedders (see below), and then project and visualize the embeddings on 3D plots.
- A web server that takes in sequences, embeds them and returns the embeddings OR visualizes the embedding spaces on interactive plots online.
- General purpose library to embed protein sequences in any python app.

We presented the bio_embeddings pipeline as a talk at ISMB 2020. You can [find it on YouTube](https://www.youtube.com/watch?v=NucUA0QiOe0&feature=youtu.be), and a copy of the poster will soon be available on [F1000](https://f1000research.com/).

## Important information

- The `albert` model weights are not publicly available yet. You can request early access by opening an issue.
- Please help us out by opening issues and submitting PRs as you see fit, this repository is actively being developed.

## Install guides

You can install the package via pip like so:

```bash
pip install bio-embeddings
```

Or directly from the source (e.g. to have the latest features):

```bash
pip install -U git+https://github.com/sacdallago/bio_embeddings.git
```

## Examples

We highly recommend you to check out the `examples` folder for pipeline examples, and the `notebooks` folder for post-processing pipeline runs and general purpose use of the embedders.

After having installed the package, you can:

1. Use the pipeline like:

    ```bash
    bio_embeddings config.yml
    ```

    A blueprint of the configuration file, and an example setup can be found in the `examples` directory of this repository.

1. Use the general purpose embedder objects via python, e.g.:

    ```python
    from bio_embeddings import SeqVecEmbedder

    embedder = SeqVecEmbedder()

    embedding = embedder.embed("SEQVENCE")
    ```

    More examples can be found in the `notebooks` folder of this repository.

## Development status

1. Pipeline stages
    - embed:
        - [x] SeqVec v1/v2 (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8)
        - [ ] Fastext
        - [ ] Glove
        - [ ] Word2Vec
        - [ ] UniRep (https://www.nature.com/articles/s41592-019-0598-1?sfns=mo)
        - [x] Albert (unpublished)
    - project:
        - [x] t-SNE
        - [x] UMAP
    
1. Web server (unpublished):
    - [x] SeqVec
    - [x] Albert (unpublished)

1. General purpose objects:
    - [x] SeqVec
    - [x] Fastext
    - [x] Glove
    - [x] Word2Vec
    - [ ] UniRep
    - [x] Albert (unpublished)


## Building a Distribution
Building the packages best happens using invoke.
If you manganage your dependecies with poetry this should be already installed.
Simply use `poetry run invoke clean build` to update your requirements according to your current status
and to generate the dist files

### Additional dependencies and steps to run the webserver

If you want to run the webserver locally, you need to have some python backend deployment experience.
You'll need a couple of dependencies if you want to run the webserver locally: `pip install dash celery pymongo flask-restx pyyaml`.

Additionally, you will need to have two instances of the app run (the backend and at least one celery worker), and both instances must be granted access to a MongoDB and a RabbitMQ or Redis store for celery.

## Contributors

- Christian Dallago (lead)
- Konstantin Schütze
- Tobias Olenyi
- Michael Heinzinger
