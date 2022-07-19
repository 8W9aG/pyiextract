from .pipeline import Pipeline
from .coreferenceresolver import CoreferenceResolver
from .svoextractor import SVOExtractor
from .oiextractor import OIExtractor
from .coreferencereducer import CoreferenceReducer
from .opennreextractor import OpenNREExtractor
from .llmextractor import LLMExtractor
from .nerreducer import NERReducer
from .subjectivityreducer import SubjectivityReducer


class FullPipeline(Pipeline):
    def __init__(self) -> None:
        super().__init__(
            [CoreferenceResolver()],
            [SVOExtractor(), OIExtractor(), OpenNREExtractor(), LLMExtractor()],
            [CoreferenceReducer(), NERReducer(), SubjectivityReducer()]
        )
