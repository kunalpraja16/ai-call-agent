**AI Call Agent** is a robust, Python-based solution designed to automate and intelligently manage incoming phone calls. Leveraging **Twilio** for call management and **OpenAI's** advanced AI models (GPT-4o-mini for dynamic conversations, Whisper for accurate transcription), this system acts as a virtual assistant for your phone line.

This project empowers you to:
*   **Automate Call Answering:** Greet callers and initiate conversations using a sophisticated AI.
*   **Engage in Dynamic AI Conversations:** Provide natural, context-aware responses to caller queries.
*   **Transcribe Speech in Real-time:** Accurately convert caller's speech to text (supports Hindi and English).
*   **Intelligently Summarize Calls:** Generate concise, actionable summaries of entire conversations.
*   **Automate Note-Taking:** Save detailed call transcripts and summaries into organized Markdown files for easy reference.
*   **Process Asynchronously:** Handle summarization and note-saving in the background, ensuring a smooth caller experience.

**How it Works:**
1.  An incoming call triggers a Twilio webhook to the Flask application.
2.  The AI agent greets the caller and responds dynamically based on the conversation flow.
3.  Caller's speech is captured, transcribed, and sent to the AI for processing.
4.  Upon call completion or explicit end signals, the full conversation is processed, summarized, and saved as a detailed note.

**Tech Stack:**
*   **Python:** Core programming language.
*   **Flask:** Lightweight web framework for handling Twilio webhooks.
*   **Twilio:** For voice calls, interactive voice response (IVR), and recording management.
*   **OpenAI:** GPT-4o-mini for AI responses, Whisper for audio transcription.
*   **`python-dotenv`:** For secure environment variable management.

This project is ideal for automating customer service inquiries, taking messages, managing routine calls, or simply ensuring no important detail is missed from your phone interactions.

