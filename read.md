Why this makes you "Job Ready"
Efficiency: Notice how we used the uploads playlist ID? A junior might search for videos by channel ID (which costs more API quota). A senior knows the "Uploads" playlist is a direct, cheaper path to the data.

Filtering Logic: Instead of overwhelming the user with 200 videos (20 videos x 10 competitors), you are only showing the Top 3 Outperformers per channel. This is "Actionable Insight."


👨‍🏫 Senior Developer Insights
CORS Middleware: Junior developers often forget this and spend hours wondering why their frontend can't see their backend. By adding it now, you are "future-proofing" your app for the Streamlit UI we will build next.

Version and Docs: Notice how we named the API and provided a description. When a recruiter opens your /docs page, it looks like a real, finished product rather than a "homework assignment."

The if __name__ == "__main__": block: This is a professional touch. It means you can run the app by simply typing python app/main.py or by using the uvicorn command.


python -m streamlit run frontend.py




# 🚀 TrendSentinel: AI-Powered YouTube Intelligence

**TrendSentinel** is a **24/7 Market Intelligence Agent** designed for YouTube creators.

It automates the tedious process of *competitive scouting* by:

- Identifying a channel’s niche  
- Finding successful competitors  
- Detecting **viral outliers** (videos statistically outperforming the channel average)

---

## 🧠 The "Why" (Problem)

Most creators spend hours doom-scrolling through competitor channels to figure out:

- *What’s working right now?*  
- *Which formats are going viral?*  
- *How can I replicate success?*

Manual scouting is:

- Slow  
- Biased  
- Often misses small channels that are exploding early  

✅ TrendSentinel solves this using **Data + AI**, delivering actionable strategy in seconds.

---

## 🛠️ Tech Stack & Architecture

TrendSentinel is built with a modular **Senior-First Architecture**, separating:

- Data Acquisition  
- Intelligence  
- Strategy Generation  

### Core Technologies

- **Backend:** FastAPI (high-performance async Python)
- **AI Engine:** OpenAI GPT-4o (structured outputs + strategy)
- **Data Source:** YouTube Data API v3
- **Frontend:** Streamlit (interactive dashboard UI)
- **Validation:** Pydantic (strong data integrity)

---

## 🏗️ How It Works (System Logic)

### 1. Identity Phase
Extracts channel metadata + latest video titles to understand the creator’s focus.

---

### 2. Intelligence Phase
An AI Agent analyzes the metadata to:

- Define a specific niche  
- Generate **5 optimized competitor search queries**

---

### 3. Scouting Phase
Uses AI-generated keywords to find the:

✅ Top 10 most relevant competitor channels

---

### 4. Performance Phase
Calculates an **Outperformance Score** for every competitor video:

\[
Score = \frac{VideoViews}{ChannelAverageViews}
\]

This reveals **viral outliers** — videos that are massively outperforming.

---

### 5. Strategy Phase
A Senior Content Strategist (AI) synthesizes viral patterns into a clear:

✅ Action Plan to beat competitors

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+
- YouTube Data API Key (Google Cloud)
- OpenAI API Key

---

### 2. Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/trend-sentinel.git
cd trend-sentinel

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key" >> .env
echo "YOUTUBE_API_KEY=your_key" >> .env

💡 Simple Explanation (The "Elevator Pitch")
"I built an AI Agent that acts as a 24/7 strategist for YouTubers. It identifies your niche, finds your top 10 competitors, and tells you exactly which of their videos are 'going viral' based on a custom outperformance score. Finally, it gives you a written strategy on how to beat them."


👨‍🏫 Talking Points for Interviewers
"Why FastAPI?": I chose FastAPI for its native async support, which is critical when making multiple external API calls to YouTube and OpenAI simultaneously.

"The Outperformance Metric": Instead of looking at raw views, I engineered a ratio-based metric. This allows the system to find trends on smaller channels that a human would usually overlook.

"Modular Design": The code is separated into Services (Logic), Routers (API), and Models (Data Rules). This makes the system easy to test and scale.


Phase 1: Data Ingestion (URL -> Metadata)

Phase 2: Reasoning (Metadata -> Niche)

Phase 3: Scouting (Niche -> Competitors)

Phase 4: Math/Logic (Competitors -> Viral Outliers)

Phase 5: Strategy (Outliers -> Action Plan)