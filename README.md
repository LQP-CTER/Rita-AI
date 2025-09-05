# Rita — Telegram AI Bot

## Introduction

Rita là một Telegram bot hỗ trợ nhiều tính năng xoay quanh AI, tìm kiếm và phân tích nội dung trực tuyến. Bot được xây dựng bằng Python, sử dụng thư viện `python-telegram-bot` và tích hợp nhiều API bên ngoài như OpenAI, RapidAPI, YouTube Data API và OpenWeatherMap.

---

## Features

* **AI Chat**: trò chuyện với AI (OpenAI GPT-4) theo ngữ cảnh, lưu lịch sử theo chat\_id.
* **Wikipedia**: `/wiki <từ khóa>` lấy tóm tắt nhanh từ Wikipedia.
* **YouTube**:

  * `/search <tên>` tìm video.
  * `/analysis_ytb <URL>` phân tích metadata.
  * `/download_ytb <URL> (mp3|mp4)` tải video/audio, hỗ trợ chuyển đổi mp4 sang mp3.
* **TikTok**:

  * `/analysis_tik <URL>` phân tích thông tin video.
  * `/download_tik <URL>` tải video không watermark.
* **Shopee**:

  * `/recommend <từ khóa>` gợi ý ngẫu nhiên một số sản phẩm.
  * `/shopee <URL>` tóm tắt chi tiết sản phẩm, phân tích sentiment mô tả.
* **Weather**: `/weather <thành phố>` hiển thị mô tả thời tiết và nhiệt độ.
* **Others**: `/doc`, `/file <id>`, `/sklearn`, `/clear`, `/help`, `/feedback`, `/leak`.

---

## Architecture & Libraries

* **Ngôn ngữ**: Python 3.9+
* **Framework chính**: `python-telegram-bot`
* **AI**: `openai`
* **Xử lý media**: `moviepy`, `pyshorteners`
* **Thông tin**: `wikipedia`, `googleapiclient`, RapidAPI, `textblob`
* **Khác**: `pandas`, `requests`, `emoji`

---

## Folder Structure

```
.
├── downloads/        # file tải về
├── documents/        # tài liệu
├── Main.py           # logic chính của bot
├── Constants.py      # chứa API_KEY Telegram
├── Article.py        # class Article
├── requirements.txt  # danh sách phụ thuộc
├── user_data.txt     # log người dùng
└── README.md
```

---

## Installation & Run

1. Cài đặt môi trường ảo (tuỳ chọn).
2. Cài phụ thuộc:

   ```bash
   pip install -r requirements.txt
   ```
3. Tạo thư mục cần thiết:

   ```bash
   mkdir -p downloads documents
   ```
4. Cấu hình API keys (qua `.env` hoặc trong code).
5. Chạy bot:

   ```bash
   python Main.py
   ```

---

## Configuration

Tạo file `.env` (khuyến nghị):

```
TELEGRAM_API_KEY=...
OPENAI_API_KEY=...
OPENWEATHER_API_KEY=...
YOUTUBE_API_KEY=...
GOOGLE_CSE_API_KEY=...
GOOGLE_CSE_CX=...
RAPIDAPI_KEY_YT=...
RAPIDAPI_KEY_TIKTOK=...
RAPIDAPI_KEY_AUTODL=...
RAPIDAPI_KEY_SHOPEE=...
```

Hoặc tạm thời đặt trực tiếp trong `Constants.py`.

---

## Logging & Privacy

* Tất cả tin nhắn được log vào `user_data.txt` (thời gian, chat\_id, username, tên đầy đủ, nội dung).
* Có thể thay thế lưu vào DB để tăng bảo mật.

---

## Legal Notes

* Tải video từ YouTube/TikTok phải tuân thủ điều khoản dịch vụ của nền tảng.
* API keys không nên commit lên repo công khai.

---

## Roadmap

* Đọc config từ `.env`
* Tách API key khỏi mã nguồn
* Hỗ trợ log bằng database
* Cải thiện error handling
* Bổ sung đa ngôn ngữ (vi/en)

---

## Contact

* Telegram: @CterLQP
