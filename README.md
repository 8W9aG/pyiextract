# pyiextract

A python library for extracting knowledge from freeform text.

## Dependencies :globe_with_meridians:

* [textacy](https://github.com/chartbeat-labs/textacy)
* spacy
* AllenNLP
* OpenNRE
* Transformers

Snippets from:

* Improving AllenNLP coreference resolution.
* Language models are knowledge graphs.

## TODO

1. Add Spacy Named Entity reducer.
2. Add subjectivity reducer (using TextBlob).
3. Add context object (to prevent spacy reprocessing) using function properties.
4. Add BLINK entity linking.
5. Add quotation extraction.
6. Add automatic translation to English (without using services).
7. Filter junk triples (use ML with G2V).
8. Deduplicate triples (use ML with G2V).
