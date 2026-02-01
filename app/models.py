from pydantic import BaseModel
from typing import List

# This model defines what 'Channel Context' looks like
class ChannelContext(BaseModel):
    channel_id: str
    title: str
    description: str
    recent_titles: List[str]

# This model defines what a 'Niche Analysis' looks like
class NicheAnalysis(BaseModel):
    primary_niche: str
    target_keywords: List[str]
    competitor_search_terms: List[str]