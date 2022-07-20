from .pipeline import Pipeline
from .coreferencenormaliser import CoreferenceNormaliser
from .svoextractor import SVOExtractor
from .oiextractor import OIExtractor
from .coreferencereducer import CoreferenceReducer
from .opennreextractor import OpenNREExtractor
from .llmextractor import LLMExtractor
from .nerreducer import NERReducer
from .subjectivityreducer import SubjectivityReducer
from .blinknormaliser import BlinkNormaliser
from .englishnormaliser import EnglishNormaliser


class FullPipeline(Pipeline):
    def __init__(self) -> None:
        super().__init__(
            [EnglishNormaliser(), CoreferenceNormaliser(), BlinkNormaliser()],
            [SVOExtractor(), OIExtractor(), OpenNREExtractor(), LLMExtractor()],
            [CoreferenceReducer(), NERReducer(), SubjectivityReducer()],
        )
