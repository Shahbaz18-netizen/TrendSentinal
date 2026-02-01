import json
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.youtube import get_channel_context, find_top_competitors, get_channel_performance
from app.services.openai_agent import analyze_channel_niche, stream_strategy_report

router = APIRouter(prefix="/analyze", tags=["Trend Analysis"])

@router.post("/")
async def start_trend_analysis(channel_url: str):
    """
    ULTRA-MODERN STREAMING WORKFLOW:
    Instead of making the user wait 20s, we send data as it happens.
    """
    async def event_generator():
        try:
            # --- STEP 1: Scouting ---
            yield f"data: {json.dumps({'step': 'Scouting Channel...', 'status': 'start'})}\n\n"
            user_context = await get_channel_context(channel_url)
            yield f"data: {json.dumps({'step': 'context_found', 'data': user_context})}\n\n"

            # --- STEP 2: Niche Analysis ---
            yield f"data: {json.dumps({'step': 'AI Brainstorming Niche...', 'status': 'progress'})}\n\n"
            niche_analysis = await analyze_channel_niche(user_context)
            yield f"data: {json.dumps({'step': 'niche_defined', 'niche': niche_analysis.primary_niche})}\n\n"

            # --- STEP 3: Competitor Scouting ---
            yield f"data: {json.dumps({'step': 'Hunting Competitors...', 'status': 'progress'})}\n\n"
            competitor_list = await find_top_competitors(
                niche_analysis.competitor_search_terms, 
                user_context['channel_id']
            )

            # --- STEP 4: Parallel Performance Analysis ---
            yield f"data: {json.dumps({'step': f'Analyzing {len(competitor_list)} Rivals...', 'status': 'progress'})}\n\n"
            tasks = [get_channel_performance(comp['channel_id']) for comp in competitor_list]
            results = await asyncio.gather(*tasks)

            all_viral_videos = []
            market_trends = []
            for i, viral_vids in enumerate(results):
                if viral_vids:
                    all_viral_videos.extend(viral_vids)
                    market_trends.append({
                        "channel": competitor_list[i]['title'],
                        "videos": viral_vids
                    })
            
            # Send the gathered market data before starting the long AI report
            yield f"data: {json.dumps({'step': 'market_data', 'trends': market_trends})}\n\n"

            # --- STEP 5: Streaming AI Strategy (The Grand Finale) ---
            yield f"data: {json.dumps({'step': 'Generating AI Strategy...', 'status': 'streaming'})}\n\n"
            
            # We yield chunks of text one by one as OpenAI generates them
            async for chunk in stream_strategy_report(all_viral_videos, niche_analysis.primary_niche):
                if chunk:
                    # We wrap the text chunk in a small JSON
                    yield f"data: {json.dumps({'step': 'strategy_chunk', 'content': chunk})}\n\n"

            yield f"data: {json.dumps({'step': 'complete', 'message': 'Analysis Finished!'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'step': 'error', 'details': str(e)})}\n\n"

    # 'text/event-stream' is the magic header for streaming
    return StreamingResponse(event_generator(), media_type="text/event-stream")