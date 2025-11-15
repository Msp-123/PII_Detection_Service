from fastapi import FastAPI, Depends
from .schemas import DetectRequest, DetectResponse, EntitySpan, RedactRequest, RedactResponse
from presidio_anonymizer import OperatorConfig
from .security import verify_api_key
from .analyzer import analyzer_engine, anonymizer_engine
from .config import settings

app = FastAPI(title="PII Detection Service", version="1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/v1/detect", response_model=DetectResponse)
def detect(req: DetectRequest, _=Depends(verify_api_key)):
    # min_score: request’te varsa onu, yoksa ayarlardan al
    min_score = req.min_score or settings.min_score

    results = analyzer_engine.analyze(
        req.text,
        entities=req.entities,
        language="en",
        score_threshold=min_score,
    )

    entities = [
        EntitySpan(
            type=r.entity_type,
            value=req.text[r.start:r.end],
            start=r.start,
            end=r.end,
            score=r.score,
        )
        for r in results
    ]

    return DetectResponse(entities=entities)


@app.post("/v1/redact", response_model=RedactResponse)
def redact(req: RedactRequest, _=Depends(verify_api_key)):

    # 1) Detect
    results = analyzer_engine.analyze(
        req.text,
        language="en",
        score_threshold=settings.min_score,
    )

    # Sadece policy.entities_to_mask listesinde olanları al
    if req.policy.entities_to_mask:
        filtered_results = [
            r for r in results if r.entity_type in req.policy.entities_to_mask
        ]
    else:
        filtered_results = results

    # 2) Operators dict
    operators = {}

    for e in filtered_results:
        # "{{ENTITY_TYPE}}" -> "{{PERSON}}" gibi olsun diye
        masked_value = req.policy.template.replace("ENTITY_TYPE", e.entity_type)

        operators[e.entity_type] = OperatorConfig(
            "replace",
            {"new_value": masked_value},
        )

    # Fallback: tanımlanmayan entity türleri için
    operators["DEFAULT"] = OperatorConfig(
        "replace",
        {"new_value": req.policy.template.replace("ENTITY_TYPE", "PII")},
    )

    # 3) Anonymize
    masked = anonymizer_engine.anonymize(
        text=req.text,
        analyzer_results=filtered_results,
        operators=operators,
    )

    return RedactResponse(masked_text=masked.text)
