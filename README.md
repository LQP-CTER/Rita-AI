# Rita - AI Telegram Bot

## 📌 Overview
Rita is an AI-powered Telegram bot designed to assist users with various tasks, including natural language conversation, AI-generated responses, web searches, and media analysis. It integrates with OpenAI, Wikipedia, YouTube, TikTok, and Shopee to provide smart assistance.

## 🚀 Features
- **AI Chatbot with OpenAI Integration**: Engage in meaningful AI-driven conversations.
- **Web Search & Wikipedia Lookup**: Retrieve relevant information with AI-powered search.
- **YouTube Video Analysis & Download**: Analyze video metadata and download in MP3/MP4 formats.
- **TikTok Video Analysis & Download**: Fetch video details and download watermark-free content.
- **Shopee Product Search & Summary**: Retrieve product recommendations and details.
- **User Activity Logging**: Store interactions for insights and improvements.
- **Weather Forecasting**: Get real-time weather updates for any city.

## 🛠️ Setup
### Prerequisites
- Python 3.8+
- Required dependencies

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/lqp-cter/rita-telegram-bot.git
   cd rita-telegram-bot
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up API keys:
   - Replace `API_KEY` in the script with your Telegram bot token.
   - Update `OpenAI API Key`, `X-RapidAPI-Key`, and `YouTube API Key`.
4. Run the bot:
   ```sh
   python main.py
   ```

## 🔧 Configuration
### Environment Variables
- `API_KEY`: Your Telegram bot API token.
- `OpenAI API Key`: API key for AI chatbot.
- `X-RapidAPI-Key`: RapidAPI key for web scraping.
- `YouTube API Key`: API key for video analysis.
- `DOWNLOAD_FOLDER`: Directory to store downloaded media files.

## 📜 Usage
### Start the Bot
To start interacting with Rita, send the `/start` command.

### AI Chatbot
Engage in AI-powered conversations:
```sh
/chat <your message>
```

### Web Search & Wikipedia Lookup
Find information easily:
```sh
/wiki <keyword>
```
```sh
/search <query>
```

### YouTube Features
- Search for videos:
  ```sh
  /search <Video Name>
  ```
- Download a video in MP3/MP4 format:
  ```sh
  /download_ytb <YouTube URL> <mp3/mp4>
  ```
- Analyze a YouTube video:
  ```sh
  /analysis_ytb <YouTube URL>
  ```

### TikTok Features
- Analyze TikTok video metadata:
  ```sh
  /analysis_tik <TikTok Video URL>
  ```
- Download TikTok video without watermark:
  ```sh
  /download_tik <TikTok Video URL>
  ```

### Shopee Product Lookup
- Search for products:
  ```sh
  /recommend <Keyword>
  ```
- Get product details from Shopee:
  ```sh
  /shopee <Shopee Product URL>
  ```

### Additional Features
- Check the weather: `/weather <City>`
- Clear chat history: `/clear`
- View available documents: `/doc`
- Fetch specific documents: `/file <Document ID>`

## 📂 File Structure
```
├── Downloads/            # Directory for downloaded media
├── main.py               # Main bot script
├── requirements.txt      # Dependencies
├── user_data.txt         # User activity log
├── README.md             # Documentation
```

## 📌 Dependencies
- `python-telegram-bot`
- `requests`
- `pandas`
- `pyshorteners`
- `openai`
- `textblob`
- `moviepy`
- `wikipedia`
- `emoji`

Install them via:
```sh
pip install -r requirements.txt
```

## 💡 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

## 🛡️ License
This project is open-source and licensed under the MIT License.

## 📬 Contact
For issues or feature requests, contact [Lê Qúy Phát](https://t.me/CterLQP).

---
Thank you for using Rita! 😊

