from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    api_key: str = Field("change-me", alias="API_KEY")
    min_score: float = Field(0.35, alias="MIN_SCORE")
    bert_model_name: str = Field("dslim/bert-base-NER", alias="BERT_MODEL_NAME")
    enable_rate_limit: bool = Field(False, alias = "ENABLE_RATE_LIMIT")


class Config:
    env_file = ".env"

settings = Settings()

