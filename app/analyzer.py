from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from .recognizers.bert_ner_recognizer import BertNerRecognizer
from .recognizers.regex_recognizers import build_regex_recognizers
from .config import settings

def build_analyzer():
    nlp_configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {"lang_code": "en", "model_name": "en_core_web_lg"}
        ]
    }

    # Create SpaCy NLP Engine
    provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
    nlp_engine = provider.create_engine()
    nlp_engine.load()

    # Recognizer registration system
    registry = RecognizerRegistry()
    registry.load_predefined_recognizers(nlp_engine=nlp_engine)

    # Add regex recognizers
    for rec in build_regex_recognizers():
        registry.add_recognizer(rec)

    # Add BERT recognizer
    bert_rec = BertNerRecognizer(settings.bert_model_name)
    registry.add_recognizer(bert_rec)

    # Initialize the AnalyzerEngine
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, registry=registry)
    return analyzer


analyzer_engine = build_analyzer()
anonymizer_engine = AnonymizerEngine()
