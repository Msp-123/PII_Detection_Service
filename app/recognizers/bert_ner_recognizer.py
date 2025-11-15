from presidio_analyzer import EntityRecognizer, RecognizerResult
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

class BertNerRecognizer(EntityRecognizer):
    def __init__(self, model_name: str):
        super().__init__(supported_entities=["PERSON", "ORG", "LOC"], name="BertNerRecognizer")
        self.pipe = pipeline("token-classification", model=model_name, aggregation_strategy="simple")

    def analyze(self, text, entities, nlp_artifacts=None):
        results = []
        if not text:
            return results
        preds = self.pipe(text)
        for p in preds:
            label = p.get("entity_group", "")
            start, end, score = int(p["start"]), int(p["end"]), float(p["score"])
            mapped = {"PER": "PERSON", "ORG": "ORGANIZATION", "LOC": "LOCATION"}.get(label, None)
            if mapped:
                results.append(RecognizerResult(entity_type=mapped, start=start, end=end, score=score))
        return results