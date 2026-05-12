# AI Interview Coach

**AI-powered technical interview practice powered by open-source LLMs (via Groq API)**

An intelligent interview simulator that conducts realistic technical interviews, provides real-time feedback on your answers, and helps you improve across multiple engineering roles.

## Live Demo

🔗 **https://ed0e3f4f30e29f.lhr.life** (open in any browser, no login required)

## Features

- **Multiple Engineering Roles**: Practice for Python Backend, Frontend, ML Engineer, or General Software Engineer interviews
- **Real-time AI Feedback**: Get immediate constructive feedback after each answer
- **Structured Rating**: Answers rated on Accuracy, Depth, and Clarity (1-5)
- **Session Persistence**: Full conversation history during each interview
- **Dark-themed UI**: Modern, sleek interface optimized for focus
- **Powered by Llama 3.3 70B**: One of the most capable open-source instruction-following models via Groq's free API tier

## How It Works

1. Choose your target engineering role
2. Start the interview session
3. Answer the AI interviewer's questions
4. Receive real-time feedback and ratings
5. Review your performance summary at the end

## Tech Stack

- **Backend**: Flask (Python)
- **AI Model**: Llama 3.3 70B Instruct via [Groq API](https://console.groq.com) (free tier)
- **Frontend**: Vanilla HTML/CSS/JS (no framework)
- **Deployment**: Docker-ready, localhost.run for local tunneling

## Setup

### Prerequisites

- Python 3.10+
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/Kaymue-commits/gemma-interview-app.git
cd gemma-interview-app

# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY="your_key_here"

# Run the app
flask run --port 5000
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Docker

```bash
docker build -t interview-coach .
docker run -p 5000:5000 -e GROQ_API_KEY=your_key interview-coach
```

### Expose with localhost.run (for live demo)

```bash
ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa -R 80:localhost:5000 ssh.localhost.run
```

## Project Structure

```
gemma-interview-app/
├── app.py              # Flask backend with Groq API integration
├── templates/
│   └── index.html      # Single-page frontend
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker deployment
└── README.md
```

## Demo Video

> Add your YouTube demo video link here

## License

MIT License
