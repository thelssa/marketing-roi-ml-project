from pydantic import BaseModel


class MarketingInput(BaseModel):
    tv: float
    radio: float
    social_media: float
    influencer: str