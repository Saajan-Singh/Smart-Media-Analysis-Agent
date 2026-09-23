# Smart-Media-Analysis-Agent

An enterprise-grade, highly deterministic AI moderation command center designed to analyze, categorize, and assess the risk of digital media assets.

MediaLens replaces slow, manual, and context-blind binary safety filters (e.g., "safe" or "flagged") with an automated pipeline. It intelligently categorizes media, extracts precise visual context, and uses natural language to explain its risk assessment reasoning—all wrapped in a pristine "Warm Orange & Pure White" enterprise UI.

🚀 The Architecture & Dashboard Experience

The application is built on a responsive, 3-column command center architecture, designed for high-throughput media auditing.

1. Media Ingestion & Dynamic Indexing (Left Column)

This module handles data intake, organization, and vector database management.

Media Upload Pipeline: A dedicated drag-and-drop zone for users to seamlessly ingest raw media files.

AI-Driven Folder Sorting: Uploaded media is automatically analyzed and sorted into dynamically generated, evenly spaced collection folders (e.g., "Transportation", "Memes", "News") based on the asset's subject matter.

Vector Database Integration: The dashboard actively tracks the connection to a local ChromaDB node, monitoring the number of indexed vectors to enable advanced semantic search and retrieval across all uploaded media.

2. Conversational Media QA Assistant (Center Column)

The interactive core where the human auditor collaborates directly with the AI.

Dynamic Empty State: When idle, the center column displays a professional prompt ("How can I assist with media analysis today?") paired with actionable feature pills. This state automatically vanishes the moment the user types their first query, keeping the interface clean and focused.

Interactive Agent Interface: A ChatGPT-style chat window allows the user to query the AI directly about the uploaded asset. Visual distinction is enforced using vibrant orange chat bubbles for user messages and soft slate for the AI, ensuring high readability for deep investigative sessions.

3. Automated Analysis Report (Right Column)

Operating as a transparent audit trail, this fixed-height, internally scrollable sidebar breaks down exactly how the model interpreted the media without breaking the page layout.

Generated Categories: Translates raw visual data into structured classifications. Driven by GPT-5-mini, it assigns accurate tags to the media (e.g., "Financial Statement" or "Railway") and displays them as soft orange pills.

Composite Risk Meter: A quantitative safety gauge that calculates a threat score based on strict moderation guidelines. The UI maps this score to a visual progress bar that shifts along a gradient from green (benign/low risk) to red (severe policy violation).

AI Moderation Reasoning: The analytical core of the dashboard. Abandoning the "black box" approach, this scrollable text module provides the AI's deterministic logic. It details exactly what is happening in the image and justifies its calculated risk score based on visual facts.

Active Image Preview: Locks the currently queried media into a fixed-height frame. This allows users to easily cross-reference the AI's text reasoning and OCR extractions against the source image, complete with an "Open Full Size" function for deep-dive manual reviews.

🧠 Advanced AI Engineering (The Secret Sauce)

To ensure this tool functions as a strict compliance auditor rather than a creative storyteller, we engineered specific solutions to counteract common LLM limitations:

Dense Captioning over Generic Tags: Relying on generic vision tags previously caused the AI to hallucinate affectionate interactions out of aggressive ones (e.g., mistaking people arguing in close proximity for a couple kissing). We upgraded the Azure AI Vision pipeline to extract Dense Captions. This feeds the LLM exact visual actions ("woman yelling," "man pointing"), resulting in flawless physical context analysis.

Deterministic Prompt Guardrails: The gpt-5-mini model operates strictly as a reasoning engine, locking the API temperature to 1.0 (highly creative) by default. To counteract this and force deterministic behavior, we implemented aggressive system prompt engineering. The model is explicitly commanded to act as a strict, literal auditor and is forbidden from inventing creative backstories, ensuring highly accurate, policy-driven moderation.

🛠️ Technology Stack

Frontend:

HTML5 & Vanilla JavaScript

Tailwind CSS (Custom grid layouts, internal scrollbars, enterprise UI tokens)

Backend & AI Pipeline:

Python & FastAPI (Async endpoints, static media serving)

ChromaDB (Local vector database for semantic search)

Azure AI Vision (OCR & Dense Captions extraction)

Azure OpenAI (gpt-5-mini for contextual reasoning and conversational QA)

💻 Getting Started

Prerequisites

Python 3.9+

Active Azure Subscription with OpenAI and Computer Vision resources deployed.
