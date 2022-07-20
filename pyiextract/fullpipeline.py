from .blinknormaliser import BlinkNormaliser
from .coreferencenormaliser import CoreferenceNormaliser
from .coreferencereducer import CoreferenceReducer
from .englishnormaliser import EnglishNormaliser
from .llmextractor import LLMExtractor
from .nerreducer import NERReducer
from .oiextractor import OIExtractor
from .opennreextractor import OpenNREExtractor
from .pipeline import Pipeline
from .subjectivityreducer import SubjectivityReducer
from .svoextractor import SVOExtractor


class FullPipeline(Pipeline):
    def __init__(self) -> None:
        super().__init__(
            [EnglishNormaliser(), CoreferenceNormaliser(), BlinkNormaliser()],
            [SVOExtractor(), OIExtractor(), OpenNREExtractor(), LLMExtractor()],
            [CoreferenceReducer(), NERReducer(), SubjectivityReducer()],
        )
