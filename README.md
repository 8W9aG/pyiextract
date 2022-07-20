# pyiextract

<a href="https://pypi.org/project/pyiextract/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/pyiextract">
</a>

A python library for extracting knowledge from raw sources.

## Architecture :triangular_ruler:

This library is built on top of an information extraction pipeline which performs the following functions:

`Pipeline` is the main protocol which defines how the various nodes in the pipeline interact and keeps track of the state of the analysis. It is responsible for taking in the raw media and outputting a document with the extracted information. The inbuilt pipelines are:

|Name|Functionality                                                         |
|----|----------------------------------------------------------------------|
|Full|Runs all the nodes in the pipeline for optimal information extraction.|

`Normaliser` is the protocol which nodes use to define ways to refine the raw media so it can be easily processed down the line. It takes the raw media as an input and outputs the same raw media with the processing applied to it.

|Name       |Functionality                                                                                                 |
|-----------|--------------------------------------------------------------------------------------------------------------|
|english    |Checks if the text is in english, or if it isn't provide translation to english if it is a supported language.|
|coreference|Resolves pronouns to their intended reference entity.                                                         |
|blink      |Links the entities mentioned in the document to global identifiers.                                           |

`Extractor` is the protocol which nodes use to extract information in clearly defined ways (such as `Triple`). These are responsible for producing as much information as possible from the raw media.

|Name   |Functionality                                                                      |
|-------|-----------------------------------------------------------------------------------|
|svo    |Finds subject verb object triples in the text (rule based approach).               |
|openie |Finds relationships between entities with attributes.                              |
|opennre|Finds structured relationships between entities (such as father).                  |
|llm    |Finds relationships between entities using large language model attention matrices.|

`Reducer` is the protocol which nodes use to remove and deduplicate the information extracted previously so it is presented to the user of the library cleanly.

|Name        |Functionality                                                 |
|------------|--------------------------------------------------------------|
|coreference |Remove any triples with a pronoun as their entity.            |
|ner         |Remove any triples where both entities are not named entities.|
|subjectivity|Remove any triples representing a subjective opinion.         |

Right now there are no efforts to use accelerated versions of these models, so unfortunately the library is slow. In the future CUDA and other acceleration efforts will be supported as well as FAISS databases.

## Dependencies :globe_with_meridians:

* [textacy](https://github.com/chartbeat-labs/textacy) - Apache 2.0 License
* [spacy](https://spacy.io/) - MIT License
* [AllenNLP](https://allenai.org/allennlp) - Apache 2.0 License
* [OpenNRE](https://github.com/thunlp/OpenNRE) - MIT License
* [Transformers](https://github.com/huggingface/transformers) - Apache 2.0 License
* [TextBlob](https://github.com/chartbeat-labs/textacy) - Apache 2.0 License
* [BLINK](https://github.com/facebookresearch/BLINK) - MIT License
* [Python Levenshtein](https://github.com/ztane/python-Levenshtein) - GPL 2.0 License
* [langdetect](https://pypi.org/project/langdetect/) - Apache 2.0 License

Snippets have also been adapted from the following repositories:

* [Improvements to AllenNLP coreference resolver](https://github.com/Laxminarayen/coreference-resolution-allenNLP/blob/main/improvements_to_allennlp_cr.ipynb) - MIT License
* [Language models are knowledge graphs](https://github.com/theblackcat102/language-models-are-knowledge-graphs-pytorch/blob/main/process.py) - MIT License

## Installation :inbox_tray:

To install from pypi:

```shell
$ pip install pyiextract
```

## Usage example :eyes:

To run the full pipeline as intended simply create a `FullPipeline` object and run the extract on it. Note that on the first run the library will attempt to download all the required models (which takes a while).

```python
import json

from pyiextract import fullpipeline

pipeline = fullpipeline.FullPipeline()
doc = pipeline.extract("Paul Allen was born on January 21, 1953, in Seattle, Washington, to Kenneth Sam Allen and Edna Faye Allen. Allen attended Lakeside School, a private school in Seattle, where he befriended Bill Gates, two years younger, with whom he shared an enthusiasm for computers. Paul and Bill used a teletype terminal at their high school, Lakeside, to develop their programming skills on several time-sharing computer systems.")
print(json.dumps([str(x) for x in doc.triples()]))
```

This produces the following:
```json
[
    "Paul Allen (11430) -> attended -> Lakeside School (121098) {svo-extractor}",
    "Paul Allen (11430) -> befriended -> Bill Gates (1584) {svo-extractor}",
    "Paul Allen (11430) -> shared -> enthusiasm {svo-extractor}",
    "Paul Allen (11430) -> attended -> Lakeside School , a private school in Seattle , Washington , where Paul Allen befriended Bill Gates , two years younger , with whom Paul Allen shared an enthusiasm for computers {openie-extractor}",
    "Paul Allen (11430) -> befriended -> Bill Gates , two years younger , with whom Paul Allen shared an enthusiasm for computers at where {openie-extractor}",
    "Paul Allen (11430) -> shared -> an enthusiasm for computers {openie-extractor}",
    "Paul Allen (11430) -> residence -> Seattle (1624986) {opennre-extractor}",
    "Paul Allen (11430) -> residence -> Washington (1807707) {opennre-extractor}",
    "Paul Allen (11430) -> father -> Kenneth Sam Allen (3014520) {opennre-extractor}",
    "Paul Allen (11430) -> mother -> Edna Faye Allen (34604) {opennre-extractor}",
    "January 21, 1953 -> location -> Seattle (1624986) {opennre-extractor}",
    "January 21, 1953 -> father -> Kenneth Sam Allen (3014520) {opennre-extractor}",
    "January 21, 1953 -> mother -> Edna Faye Allen (34604) {opennre-extractor}",
    "Seattle (1624986) -> located in the administrative territorial entity -> Washington (1807707) {opennre-extractor}",
    "Seattle (1624986) -> head of government -> Kenneth Sam Allen (3014520) {opennre-extractor}",
    "Seattle (1624986) -> mother -> Edna Faye Allen (34604) {opennre-extractor}",
    "Washington (1807707) -> head of government -> Kenneth Sam Allen (3014520) {opennre-extractor}",
    "Kenneth Sam Allen (3014520) -> spouse -> Edna Faye Allen (34604) {opennre-extractor}",
    "Paul Allen (11430) -> field of work -> Paul Allen (11430) {opennre-extractor}",
    "Paul Allen (11430) -> bear -> January {llm-extractor}",
    "Paul Allen (11430) -> bear -> Seattle (1624986) {llm-extractor}",
    "Paul Allen (11430) -> bear -> Washington (1807707) {llm-extractor}",
    "Paul Allen (11430) -> bear -> Kenneth Sam Allen (3014520) {llm-extractor}",
    "Paul Allen (11430) -> bear -> Edna Faye Allen (34604) {llm-extractor}",
    "Lakeside School (121098) -> befriend -> shared {llm-extractor}",
    "Lakeside School (121098) -> befriend -> shared {llm-extractor}",
    "Lakeside School (121098) -> befriend -> Bill Gates (1584) {llm-extractor}",
    "Lakeside School (121098) -> befriend -> shared {llm-extractor}",
    "Lakeside School (121098) -> befriend -> an enthusiasm {llm-extractor}",
    "Lakeside School (121098) -> befriend -> computers {llm-extractor}",
    "a private school -> befriend -> Bill Gates (1584) {llm-extractor}",
    "Seattle (1624986) -> befriend -> shared {llm-extractor}",
    "Seattle (1624986) -> befriend -> shared {llm-extractor}",
    "Seattle (1624986) -> befriend -> Bill Gates (1584) {llm-extractor}",
    "Seattle (1624986) -> befriend -> shared {llm-extractor}",
    "Seattle (1624986) -> befriend -> an enthusiasm {llm-extractor}",
    "Seattle (1624986) -> befriend -> computers {llm-extractor}",
    "Washington (1807707) -> befriend -> shared {llm-extractor}",
    "Washington (1807707) -> befriend -> shared {llm-extractor}",
    "Washington (1807707) -> befriend -> Bill Gates (1584) {llm-extractor}",
    "Washington (1807707) -> befriend -> shared {llm-extractor}",
    "Washington (1807707) -> befriend -> an enthusiasm {llm-extractor}",
    "Washington (1807707) -> befriend -> computers {llm-extractor}",
    "Paul Allen (11430) -> share -> an enthusiasm {llm-extractor}",
    "Paul Allen (11430) -> share -> computers {llm-extractor}",
    "Paul Allen (11430) -> use -> a teletype terminal {llm-extractor}",
    "Paul Allen (11430) -> share -> a teletype terminal {llm-extractor}",
    "Paul Allen (11430) -> use -> Lakeside (52851) {llm-extractor}",
    "Paul Allen (11430) -> share -> Lakeside (52851) {llm-extractor}",
    "Paul Allen (11430) -> develop -> Paul and Bill's programming skills {llm-extractor}",
    "Paul Allen (11430) -> use -> Paul and Bill's programming skills {llm-extractor}",
    "Paul Allen (11430) -> share -> Paul and Bill's programming skills {llm-extractor}",
    "Paul Allen (11430) -> develop -> several time-sharing computer systems {llm-extractor}",
    "Paul Allen (11430) -> use -> several time-sharing computer systems {llm-extractor}",
    "Paul Allen (11430) -> share -> several time-sharing computer systems {llm-extractor}",
    "Bill Gates (1584) -> share -> an enthusiasm {llm-extractor}",
    "Bill Gates (1584) -> share -> computers {llm-extractor}",
    "Bill Gates (1584) -> use -> a teletype terminal {llm-extractor}",
    "Bill Gates (1584) -> share -> a teletype terminal {llm-extractor}",
    "Bill Gates (1584) -> use -> Lakeside (52851) {llm-extractor}",
    "Bill Gates (1584) -> share -> Lakeside (52851) {llm-extractor}",
    "Bill Gates (1584) -> develop -> Paul and Bill's programming skills {llm-extractor}",
    "Bill Gates (1584) -> use -> Paul and Bill's programming skills {llm-extractor}",
    "Bill Gates (1584) -> share -> Paul and Bill's programming skills {llm-extractor}",
    "Bill Gates (1584) -> develop -> several time-sharing computer systems {llm-extractor}",
    "Bill Gates (1584) -> use -> several time-sharing computer systems {llm-extractor}",
    "Bill Gates (1584) -> share -> several time-sharing computer systems {llm-extractor}",
    "an enthusiasm -> use -> Lakeside (52851) {llm-extractor}",
    "computers -> use -> Lakeside (52851) {llm-extractor}",
    "Lakeside (52851) -> develop -> Paul and Bill's programming skills {llm-extractor}",
    "Lakeside (52851) -> develop -> several time-sharing computer systems {llm-extractor}"
]
```

## License :memo:

The project is available under the [GPL 2.0 License](LICENSE).

## TODO

1. Filter junk triples (use ML with G2V).
2. Deduplicate triples (use ML with G2V).
3. Create a training mode that can be used to fine-tune the underlying models.
