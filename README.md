# Asky - AI Personal Assistant

Asky is an intelligent web application designed to act as an AI-powered personal assistant. The application integrates with **Asky**, a virtual assistant agent powered by the **DeepSeek LLM** and configured through dynamic prompts (definitions and training examples) managed in a **Supabase database**.

---

## Key Features

1. **Dynamic Rule Customization**: Manage definition prompts and training datasets stored in Supabase in real time directly from the dashboard.
2. **Interactive Playground**: Send questions or prompts to Asky and receive direct text answers generated using your custom rules.
3. **Bilingual Support**: Instant toggle between English (EN) and Vietnamese (VI) localizations.
4. **Developer Tools**: Easily query the assistant via the underlying `/api/chien/question` API.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Supabase account and database table
- DeepSeek API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/truong0vanchien/botchien.git
   cd botchien
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   Create a `.env` file in the root directory and add the following environment variables:
   ```env
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   DEEPSEEK_MODEL_NAME=deepseek-chat
   APP_LIST=chien
   SUBJECT_LIST=asky
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://localhost:5000`.

### Running with Docker

Alternatively, you can build and run the application using Docker:

1. **Build the Docker image**:
   ```bash
   docker build -t asky-assistant .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -d -p 5000:5000 --env-file .env asky-assistant
   ```

---

## Architecture & Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Jinja Templates, Tailwind CSS / Vanilla CSS, JavaScript (Vanilla)
- **Database**: Supabase (PostgreSQL)
- **AI Integration**: OpenAI Python client connecting to DeepSeek APIs