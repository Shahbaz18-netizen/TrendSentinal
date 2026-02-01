import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.models import NicheAnalysis 

load_dotenv()

# Async client is a MUST for streaming in FastAPI
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_channel_niche(channel_data: dict) -> NicheAnalysis:
    """
    LOGIC: This part remains structured (non-streaming) because 
    we need the full Niche/Keywords to start the scouting phase.
    """
    system_message = (
        "You are a world-class YouTube Strategist. Define the channel's specific niche "
        "and provide 5 high-intent search terms to find competitors."
    )

    user_content = f"""
    Channel: {channel_data['title']}
    Bio: {channel_data['description']}
    Recent Videos: {', '.join(channel_data['recent_titles'])}
    """

    completion = await client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content},
        ],
        response_format=NicheAnalysis,
    )
    return completion.choices[0].message.parsed

async def stream_strategy_report(viral_videos: list, user_niche: str):
    """
    THE REAL STREAMER: 
    Instead of returning a full string, this 'yields' chunks of text.
    """
    system_prompt = f"""
    You are a Senior YouTube Growth Expert. Analyze these viral outliers 
    in the {user_niche} niche and provide 3 specific content blueprints.
    Focus on WHY these worked and HOW the user can replicate them.
    and also provide 3 CONTENT BLUEPRINTS: Suggest 3 video ideas. For each idea, provide:
    - A 'Click-Bait' (but honest) Title.
    - The 'Viral Hook' (Why will people click?).
    - The 'Value Proposition' (Why will they stay?
    """
    
    titles_metadata = "\n".join([
        f"- {v['title']} ({v['outperformance_score']}x views)" 
        for v in viral_videos
    ])

    # 1. We enable 'stream=True'
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Trending videos:\n{titles_metadata}"}
        ],
        stream=True  # <--- MAGIC PARAMETER
    )

    # 2. We loop through the response stream
    async for chunk in response:
        # Extract the text fragment (delta)
        content = chunk.choices[0].delta.content
        if content:
            # yield it to the FastAPI event_generator
            yield content