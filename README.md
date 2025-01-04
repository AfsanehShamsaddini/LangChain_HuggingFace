
# Chatbot with Persistent History

This repository contains a chatbot implementation that utilizes the Hugging Face GPT-2 model for conversation, while storing chat history in an SQLite database for continuity across sessions. This chatbot is designed to provide concise answers and maintain a history of interactions.

## Getting Started

To run this project, make sure you have Python 3.x installed. Follow the instructions to set up the required environment.

## Prerequisites

- Python 3.x
- langchain
- python-dotenv
- sqlite3 (comes built-in with Python)

You can install the required libraries using pip:

```bash
pip install langchain python-dotenv
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatbot-with-history.git
   cd chatbot-with-history
   ```

2. Create a `.env` file in the root directory of the project and add your Hugging Face API token:
   ```
   hf_token=your_hugging_face_token
   ```

## Usage

To run the chatbot, simply execute the following command:

```bash
python Langchain_memory.py
```

## How It Works

- **Chat History**: The chatbot stores the conversation history in a SQLite database, allowing for better context management across user sessions.
- **AI Model**: The implementation uses a Hugging Face GPT-2 model configured with parameters to optimize responses for brevity and relevance.
- **Dynamic Chat Interface**: The chatbot accepts user input, processes it, retrieves the session history, generates a response from the AI model, and updates the history.

### Key Components

1. **Database Initialization**: The chatbot initializes a SQLite database on startup to store chat history.

2. **Chat Session Management**: Each conversation session is identified by a unique session ID. The bot retrieves the chat history based on this session ID.

3. **AI Interaction**: The user input is parsed into a prompt for the Hugging Face model, which generates a response.

4. **Response Formatting**: Responses from the model are parsed and formatted before being printed back to the user.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to contribute or reach out for any questions or enhancements!
```

### Notes:
- Replace `https://github.com/yourusername/chatbot-with-history.git` with the actual URL of your GitHub repository.
- Ensure that any sensitive information, such as API tokens, is kept secure and not shared publicly.
- You may want to highlight any additional features or functionalities your chatbot offers, such as specific training data or response tuning parameters.
