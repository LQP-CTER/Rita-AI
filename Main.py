# Import các thư viện chuẩn của Python
import logging
import os
import re
import time

# Import các thư viện mạng và xử lý dữ liệu
import pandas as pd
import requests
import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pyshorteners import Shortener
# Import các thư viện liên quan đến AI và xử lý media
import openai
from moviepy.editor import AudioFileClip
import wikipedia
import emoji
from textblob import TextBlob
# Import các thư viện liên quan đến Telegram
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Import thư viện nội bộ
import Constants as keys


# Để biết bot chạy hay chưu
print("Rita Starting....................")

openai.api_key = "*******************************8"

chat_history = {}

# Web search
def send_message(update, context, text, parse_mode='Markdown'):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=parse_mode)

def log_error(message):
    logging.error(message)

def search_web(query):
    URL = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': 'AIzaSyArxWVCjeptceCUybUCF_0LUwSwWz_jTAI',
        'cx': '438a965e6f00e4be1',
        'q': query,
        'num': 3
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()  # Sẽ ném ra lỗi nếu request không thành công
        result = response.json()

        links = []
        for item in result.get("items", []):
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet", "Không có mô tả.").replace('\n', ' ')
            links.append(f"{title}:\n{snippet}\nLink: {link}")

        return "\n\n".join(links) if links else "Không tìm được thông tin tham khảo ấy."
    except requests.RequestException as e:
        logging.error(f"Lỗi kết nối tới API: {str(e)}")
        return f"Lỗi kết nối tới API: {str(e)}"
    except Exception as e:
        logging.error(f"Lỗi không xác định: {str(e)}")
        return f"Lỗi không xác định: {str(e)}"
# Các lib
documents = {
    "doc1": "./documents/Numpy_Python_Cheat_Sheet.pdf",
    "doc2": "./documents/Pandas_Cheat_Sheet.pdf",
    "doc3": "./documents/Python_Matplotlib_Cheat_Sheet.pdf",
    "doc4": "./documents/Introduction_R.pdf",
    "doc5": "./documents/Support-R.pdf",
    "doc6": "./documents/H1-2021 - Vietnam Security report.pdf",
}
person = {
    "****": "**********",
    }


def send_typing(update: Update, context: CallbackContext, duration=2):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    time.sleep(duration)

def get_response(chat_id, message_text):
    message_text = message_text.lower().strip()
    person_response = handle_personal_info(message_text)
    if person_response:
        return person_response

    if "link tham khảo" in message_text:
        search_query = message_text.replace('link tham khảo', '').strip()
        return get_search_link(search_query)

    return handle_openai_response(chat_id, message_text)

def handle_personal_info(query):
    for key, description in person.items():
        if re.search(r'\b{}\b'.format(re.escape(key)), query):
            return f"Người tên {key} là {description}\n"
    return None

def get_search_link(query):
    search_result = search_web(query)
    return f"Đây là link tham khảo bạn yêu cầu: {search_result}"

def handle_openai_response(chat_id, message_text):
    system_message = {
        "role": "system",
        "content": "Bạn tên là Rita, một model AI được phát triển bởi Lê Qúy Phát. Bạn vui tính và hay chọc ghẹo."
    }

    # Giới hạn lịch sử trò chuyện ở 5 tin nhắn gần nhất
    MAX_HISTORY_LENGTH = 20
    if chat_id not in chat_history:
        chat_history[chat_id] = [system_message]
    elif len(chat_history[chat_id]) > MAX_HISTORY_LENGTH:
        chat_history[chat_id] = chat_history[chat_id][-MAX_HISTORY_LENGTH:]
        chat_history[chat_id].insert(0, system_message)
    else:
        chat_history[chat_id].insert(0, system_message)

    chat_history[chat_id].append({"role": "user", "content": message_text})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=chat_history[chat_id],
        max_tokens=500,  # Giới hạn độ dài của câu trả lời
    )
    return response['choices'][0]['message']['content'].strip()

'''Nhóm lệnh lấy tài liệu'''
# Gửi tài liệu
def send_document(update, context):
    # Lấy tên tài liệu từ tin nhắn của người dùng
    document_name = ' '.join(context.args)

    # Kiểm tra xem tên tài liệu có trong dictionary không
    if document_name in documents:
        with open(documents[document_name], 'rb') as file:
            context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    else:
        update.message.reply_text('Xin lỗi, tài liệu bạn yêu cầu không có sẵn. Hãy kiểm tra lại thư viện\n')

# Danh sách tài liệu
def display_documents(update: Update, context: CallbackContext):
    documents = [
        "📘 doc1 - Tài liệu về Database Management System",
        "📗 doc2 - Báo cáo An ninh mạng của Việt Nam năm 2021",
        "📙 doc3 - Numpy Python Cheat Sheet",
        "📔 doc4 - Pandas Python Cheat Sheet",
        "📓 doc5 - Demo quy trình khai thác dữ liệu bằng Python",
        "📒 doc6 - Matplotlib Python Cheat Sheet",
        "📙 doc7 - Python Interview Questions 🐍",
    ]

    # Tạo chuỗi thông báo
    header = "📚 *Thư viện tài liệu hiện tại:* 📚\n\n"
    message = header + "\n".join(documents) + "\n\n" + \
              "🔄 Danh sách tài liệu sẽ được cập nhật liên tục mỗi tuần nhé 😉."

    # Gửi thông báo
    update.message.reply_text(message, parse_mode='Markdown')


# Function xem dự báo thời tiết
def get_weather(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.message.reply_text("☀️ Vui lòng cung cấp tên thành phố. Ví dụ: /weather Hà Nội")
        return

    city = ' '.join(args)
    api_key = '********************************'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        reply_text = (f"🌆 Thành phố: {city}\n"
                      f"🌥️ Thời tiết hiện tại: {weather.capitalize()}\n"
                      f"🌡️ Nhiệt độ: {temperature}°C\n"
                      f"Hy vọng bạn có một ngày tuyệt vời để đi chơi với 'ai đó' nhé 😢.")
    else:
        reply_text = "🚫 Không tìm được thông tin cho thành phố này. Xin vui lòng nhập lại tên thành phố mà không dùng dấu."

    update.message.reply_text(reply_text)

""" Nhóm command cho Youtube"""

DOWNLOAD_FOLDER = './downloads'

def sanitize_filename(filename):
    # Replace any characters that are invalid in filenames with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def download(update: Update, context: CallbackContext):
    args = context.args
    if len(args) == 2 and ('youtube.com/watch?v=' in args[0] or 'youtu.be/' in args[0]) and args[1].lower() in ['mp3',
                                                                                                                'mp4']:
        video_url, file_format = args[0], args[1].lower()
        video_id = extract_video_id(video_url)
        if not video_id:
            update.message.reply_text("Invalid YouTube URL.")
            return

        update.message.reply_text('Downloading video, please wait...')

        # Use the API to get the download link
        url = "https://yt-api.p.rapidapi.com/dl"
        querystring = {"id": video_id}
        headers = {
            "x-rapidapi-key": "*********************************",
            "x-rapidapi-host": "yt-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code != 200:
            update.message.reply_text('Failed to fetch download link.')
            return

        data = response.json()
        video_format = data['formats'][0] if 'formats' in data else None

        if not video_format:
            update.message.reply_text("Failed to get video download link.")
            return

        download_link = video_format['url']

        try:
            # Sanitize the filename
            file_name = sanitize_filename(f"{data['title']}.mp4")
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            response = requests.get(download_link, stream=True)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            # Convert to MP3 if requested
            if file_format == 'mp3':
                mp3_file_path = file_path.replace('.mp4', '.mp3')
                audio_clip = AudioFileClip(file_path)
                audio_clip.write_audiofile(mp3_file_path)
                audio_clip.close()

                # Send the MP3 file
                context.bot.send_audio(chat_id=update.message.chat_id, audio=open(mp3_file_path, 'rb'))

                # Clean up
                os.remove(mp3_file_path)
            else:
                # Send the MP4 file
                context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'))

            # Clean up
            os.remove(file_path)
            update.message.reply_text('Download and conversion completed successfully!')
        except Exception as e:
            update.message.reply_text(f"An error occurred during download or conversion: {e}")
    else:
        update.message.reply_text('Please enter a valid YouTube link and format (mp3 or mp4).')


def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    if "youtube.com/watch?v=" in url:
        return re.search('v=([a-zA-Z0-9_-]{11})', url).group(1)
    elif "youtu.be/" in url:
        return url.split("/")[-1]
    else:
        return None


# Search Music
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cấu hình API key và khởi tạo client
YOUTUBE_API_KEY = '***************************'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

# Hàm tìm kiếm video nhạc
def search_music(song_name):
    try:
        # Tìm video trên YouTube
        search_response = youtube.search().list(
            q=song_name,
            part='id,snippet',
            maxResults=1,
            type='video'
        ).execute()

        # Lấy ID video đầu tiên tìm thấy
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                return f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"

        return None
    except HttpError as e:
        logger.error(f"HTTP Error occurred: {e}")
        return None

# Search video youtube
def Youtube_search(update: Update, context: CallbackContext) -> None:
    args = context.args
    if not args:
        update.message.reply_text("🎵 Vui lòng thêm tên bài hát sau câu lệnh. Ví dụ: /play Imagine Dragons Believer")
        return

    song_name = ' '.join(args)
    song_url = search_music(song_name)

    if song_url:
        update.message.reply_text(f"🔗 Đây là link nhạc bạn yêu cầu: {song_url}")
    else:
        update.message.reply_text("🚫 Không tìm thấy bài hát nào. Vui lòng thử lại với từ khóa khác!")

def extract_video_id(url):
    """Trích xuất ID video từ URL."""
    if "youtube.com/watch?v=" in url:
        return re.search('v=([a-zA-Z0-9_-]{11})', url).group(1)
    elif "youtu.be/" in url:
        return url.split("/")[-1]
    else:
        return None
# Phân tích video Youtube
def analyze_video(update, context):
    """Phân tích thông tin video từ YouTube."""
    video_url = context.args[0] if context.args else ''
    video_id = extract_video_id(video_url)
    if not video_id:
        update.message.reply_text("⚠️ Vui lòng cung cấp URL video YouTube hợp lệ.")
        return

    try:
        video_response = youtube.videos().list(
            id=video_id,
            part='id,snippet,statistics'
        ).execute()

        # Giả sử video tồn tại và API không trả về lỗi
        if 'items' in video_response and video_response['items']:
            video_data = video_response['items'][0]

            video_info = {
                'title': video_data['snippet']['title'],
                'description': video_data['snippet']['description'],
                'channel_title': video_data['snippet']['channelTitle'],
                'publish_time': video_data['snippet']['publishedAt'],
                'view_count': video_data['statistics']['viewCount'],
                'like_count': video_data['statistics'].get('likeCount', 'Không có thông tin'),
                'dislike_count': video_data['statistics'].get('dislikeCount', 'Không có thông tin'),
                'comment_count': video_data['statistics']['commentCount']
            }

            response_message = (f"🎬 Tiêu đề: {video_info['title']}\n"
                                f"📄 Mô tả: {video_info['description'][:150]}... (rút gọn)\n"
                                f"👤 Chủ kênh: {video_info['channel_title']}\n"
                                f"🕒 Thời gian xuất bản: {video_info['publish_time']}\n"
                                f"👁️ Lượt xem: {video_info['view_count']}\n"
                                f"👍 Lượt thích: {video_info['like_count']}\n"
                                f"👎 Lượt không thích: {video_info['dislike_count']}\n"
                                f"💬 Số bình luận: {video_info['comment_count']}"
            )

            update.message.reply_text(response_message)
        else:
            update.message.reply_text("Video không tồn tại hoặc đã xảy ra lỗi khi truy vấn thông tin.")
    except HttpError as e:
        logger.error(f"HTTP Error occurred: {e}")
        update.message.reply_text("Đã xảy ra lỗi khi kết nối với YouTube API.")

'''Nhóm command cho Tiktok'''

# Analyze video tiktok
def analyze_tiktok(update, context):
    """Phân tích video TikTok với thêm thông tin và rút gọn link"""
    try:
        video_url = context.args[0]
        api_url = "https://tiktok-scraper7.p.rapidapi.com/"
        querystring = {"url": video_url}
        headers = {
            "X-RapidAPI-Key": "***********************",  # Thay bằng API key của bạn
            "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
        }

        response = requests.get(api_url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        if data['code'] == 0:
            video_data = data['data']

            # Lấy thông tin video
            title = video_data.get('title', "Không có tiêu đề")
            author_nickname = video_data['author']['nickname']
            music_title = video_data['music_info'].get('title', "Không có nhạc nền")
            hashtags = [f"#{tag}" for tag in video_data['title'].split() if tag.startswith('#')]
            view_count = video_data.get('play_count', 0)
            like_count = video_data.get('digg_count', 0)
            comment_count = video_data.get('comment_count', 0)
            share_count = video_data.get('share_count', 0)
            download_count = video_data.get('download_count', 0)
            duration = video_data.get('duration', 0)
            create_time = video_data.get('create_time', 0)
            region = video_data.get('region', "Không rõ")

            # Lấy URL video và rút gọn link HD (nếu có thể)
            video_url_hd = video_data.get('hdplay', video_data.get('play', None))
            try:
                with requests.get("https://tinyurl.com", timeout=2) as response:
                    response.raise_for_status()
                    shortener = Shortener()
                    video_url_hd = shortener.tinyurl.short(video_url_hd)
            except requests.RequestException:
                pass  # Bỏ qua rút gọn URL nếu TinyURL không khả dụng

            # Xây dựng thông điệp phản hồi
            response_message = f"""
                🎬 Tiêu đề: {title}
                👤 Tác giả: {author_nickname}
                🎵 Nhạc nền: {music_title}
                # Hashtags: {' '.join(hashtags)}
                👁️ Lượt xem: {view_count}
                👍 Lượt thích: {like_count}
                💬 Bình luận: {comment_count}
                🔁 Chia sẻ: {share_count}
                ⬇️ Tải xuống: {download_count}
                ⏱️ Thời lượng: {duration} giây
                📅 Ngày đăng: {time.strftime('%Y-%m-%d', time.localtime(create_time))}
                🌎 Khu vực: {region}
            """
            if video_url_hd:
                response_message += f"\n🔗 Link HD: {video_url_hd}"

            update.message.reply_text(response_message)

        else:
            update.message.reply_text("Lỗi: Không thể lấy thông tin video.")

    except requests.RequestException as e:
        update.message.reply_text(f"Lỗi mạng: {e}")
    except Exception as e:
        update.message.reply_text(f"Lỗi: {e}")


# Download video tiktok without watermark
def download_tiktok_video(video_url, download_folder="Downloads"):
    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    payload = {"url": video_url}
    headers = {
        "x-rapidapi-key": "******************************",
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'medias' not in data or not data['medias']:
            raise ValueError("API không trả về URL video")

        # Tìm URL video không có watermark
        video_download_url = None
        for media in data['medias']:
            if media['type'] == 'video' and media['quality'] == 'hd_no_watermark':
                video_download_url = media['url']
                break

        if not video_download_url:
            raise ValueError("Không tìm thấy video không có watermark")

        video_title = data.get('title', 'tiktok_video')

        os.makedirs(download_folder, exist_ok=True)
        file_path = os.path.join(download_folder, f"{video_title}.mp4")

        with requests.get(video_download_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return file_path

    except requests.RequestException as e:
        raise Exception(f"Lỗi mạng: {e}")

    except Exception as e:
        raise Exception(f"Lỗi: {e}")

# Command download video tiktok
def tiktok_dl(update: Update, context: CallbackContext) -> None:
    """Xử lý lệnh /tiktok_dl để tải video TikTok."""
    args = context.args
    if not args:
        update.message.reply_text("Vui lòng cung cấp URL video TikTok sau lệnh /tiktok_dl")
        return

    video_url = args[0]
    try:
        file_path = download_tiktok_video(video_url)
        with open(file_path, 'rb') as f:
            context.bot.send_video(chat_id=update.effective_chat.id, video=f)
        # Xóa file video sau khi gửi
        os.remove(file_path)
    except Exception as e:
        update.message.reply_text(f"Lỗi: {e}")

"""Nhóm lệnh của Shopee"""
def recommend_product(update, context):
    args = context.args
    if not args:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Vui lòng nhập từ khóa tìm kiếm. 😕")
        return

    keyword = " ".join(args)
    url = "https://shopee-e-commerce-data.p.rapidapi.com/shopee/search/items/v2"
    querystring = {"site": "vn", "keyword": keyword, "page": "1", "pageSize": "30"}
    headers = {
        "X-RapidAPI-Key": "****************************",  # Thay bằng API Key của bạn
        "X-RapidAPI-Host": "shopee-e-commerce-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if data['code'] == 200:
        items = data['data']['items']
        if items:
            num_products = min(7, len(items))
            random_products = random.sample(items, num_products)
            message = emoji.emojize("✨ Gợi ý sản phẩm: ✨\n\n")
            for product in random_products:
                title = product['title']
                link = f"https://shopee.vn/product/{product['shop_id']}/{product['item_id']}"
                message += f"- **{title}** {emoji.emojize(':shopping_cart:')}\n"
                message += f"  * Giá: {product['price_info']['price']} {product['currency']} {emoji.emojize(':money_bag:')}\n"

                # Xử lý trường hợp không có rating_star hoặc lỗi kiểu dữ liệu
                try:
                    rating = float(product['rating_star'])
                    message += f"  * Đánh giá: {rating:.1f} sao {emoji.emojize(':star:')}\n"
                except KeyError:
                    message += f"  * Đánh giá: Không có đánh giá {emoji.emojize(':question:')}\n"
                except TypeError:
                    message += f"  * Đánh giá: Lỗi dữ liệu đánh giá {emoji.emojize(':warning:')}\n"

                message += f"  [Xem chi tiết]({link}) {emoji.emojize(':link:')}\n\n"

            context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Không tìm thấy sản phẩm nào. 😔")
    else:
        # Cung cấp thông tin lỗi API chi tiết hơn
        error_message = data.get('message', "Lỗi không xác định")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Lỗi khi truy cập API Shopee. ☹️\nChi tiết lỗi: {error_message}")

def shopee(update, context):
    # Lấy URL sản phẩm từ lệnh
    url_san_pham = context.args[0]

    url = "https://shopee-e-commerce-data.p.rapidapi.com/shopee/item_detail_by_url/v2"
    payload = {"url": url_san_pham}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "****************************",
        "X-RapidAPI-Host": "shopee-e-commerce-data.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # Kiểm tra mã trạng thái
    if data["code"] == 200:
        # Lấy thông tin sản phẩm
        product_data = data["data"]
        title = product_data["title"]
        price = product_data["price_info"]["price"]
        currency = product_data["currency"]
        url = product_data["product_url"]
        brand = product_data["brand"]
        sold_count = product_data["sold_count"]
        rating_star = product_data["rating_star"]
        # ... (Lấy thêm thông tin khác)

        # Trích xuất thuộc tính sản phẩm
        attributes = {}
        for attr in product_data["attributes"]:
            attributes[attr["name"]] = attr["value"]

        # Tạo thông báo
        message = f"""
            **️⃣ *{title}*
            -------------
            🛍️ **Thương hiệu:** {brand}
            💰 **Giá:** {price} {currency}
            📈 **Đã bán:** {sold_count}
            🌟 **Đánh giá:** {rating_star:.1f}
            🔗 **Link:** {url}
            ------------
            📑 **Thông tin chi tiết:**
            """
        for name, value in attributes.items():
            message += f"- {name}: {value}\n"

        # Phân tích sentiment từ phần mô tả sản phẩm
        if "details" in product_data:
            blob = TextBlob(product_data["details"])
            sentiment = blob.sentiment.polarity
            if sentiment > 0:
                message += "\n**Sentiment:** Tích cực"
            elif sentiment < 0:
                message += "\n**Sentiment:** Tiêu cực"
            else:
                message += "\n**Sentiment:** Trung lập"

        # Gửi hình ảnh đầu tiên (nếu có)
        if product_data["main_imgs"]:
            update.message.reply_photo(product_data["main_imgs"][0])

    else:
        message = "❌ Không tìm thấy thông tin sản phẩm."

    # Gửi thông báo
    update.message.reply_text(message, parse_mode="Markdown")

# Start bot
def start_command(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.username or f"{update.message.from_user.first_name} {update.message.from_user.last_name}"

    # Lời chào với emoji
    greeting = emoji.emojize(f"👋 Xin chào {user_name}, tôi là Rita (v2.5.2) đây!🤖 \nBạn cần Rita hỗ trợ gì nào? 🤔\n\n")

    # Nhóm lệnh với emoji và Markdown
    shopee_commands = emoji.emojize("- Nhóm lệnh của Shopee: 🛍️\n")
    shopee_commands += "  • Tìm kiếm sản phẩm: `/recommend <Từ khóa>` \n"
    shopee_commands += "  • Tóm tắt sản phẩm: `/shopee <URL sản phẩm>` \n\n"

    tiktok_commands = emoji.emojize("- Nhóm lệnh của Tiktok: 🎧\n")
    tiktok_commands += "  • Phân tích video: `/analysis_tik <Link TikTok>` \n"
    tiktok_commands += "  • Tải video: `/download_tik <Link TikTok>` \n\n"

    youtube_commands = emoji.emojize("- Nhóm lệnh của Youtube: 🎥\n")
    youtube_commands += "  • Tìm kiếm video: `/search <Tên video>` \n"
    youtube_commands += "  • Tải video: `/download_ytb <URL Youtube> (<mp3> hoặc <mp4>)` \n"
    youtube_commands += "  • Phân tích video: `/analysis_ytb <URL Youtube>` \n\n"

    document_commands = emoji.emojize("- Nhóm lệnh về Tài liệu (Tạm khóa): 📂\n")
    document_commands += "  • Xem danh sách: `/doc` \n"
    document_commands += "  • Lấy file tài liệu: `/file <ID tài liệu>` \n\n"

    other_commands = emoji.emojize("- Nhóm lệnh khác: 🔄\n")
    other_commands += "  • Kiểm tra thời tiết: `/weather <Thành phố>` \n"
    other_commands += "  • Tìm kiếm Wikipedia: `/wiki <Từ khóa>` \n"
    other_commands += "  • Kết thúc chủ đề: `/clear` \n\n"

    support_commands = emoji.emojize("- Nhóm lệnh hỗ trợ: 🆘\n")
    support_commands += "  • Xem hướng dẫn: `/help` \n"
    support_commands += "  • Gửi phản hồi: `/feedback <Nội dung>` \n\n"

    # Footer với emoji
    footer = emoji.emojize(
        "💖 Rita hiện đang được phát triển. Nếu có lỗi hoặc bot không hoạt động, vui lòng thông báo cho tôi nhé: https://t.me/CterLQP \n                                               ~CterLQP~ ")

    # Gửi thông tin đã được định dạng
    update.message.reply_text(
        greeting + shopee_commands + tiktok_commands + youtube_commands + document_commands + other_commands + support_commands + footer,
        parse_mode='Markdown')

# Hỗ trợ tìm kiếm câu lệnh
def help_command(update: Update, context: CallbackContext):
    help_text = emoji.emojize(
        "🤖 Rita sẵn sàng hỗ trợ bạn!  🙋‍♀️\n\n"
        "✨ Bắt đầu:\n"
        "   `/start` 🚀 - Gặp gỡ Rita và khám phá các tính năng.\n\n"
        "📚 Tìm kiếm thông tin:\n"
        "   `/wiki <từ_khóa>` 🌐 - Khám phá thế giới Wikipedia.\n\n"
        "🎧🎬 Video & Âm nhạc:\n"
        "   `/search <tên_video>` 🎶 - Tìm kiếm video Youtube.\n"
        "   `/download <link_youtube> (<mp3>|<mp4>)` 📥 - Tải video Youtube.\n"
        "   `/analysis <link_youtube>` 🧐 - Phân tích video Youtube.\n"
        "   `/analysis_tik <link_tiktok>` 🧐 - Phân tích video Tiktok.\n"
        "   `/download_tik <link_tiktok>` 📥 - Tải video Tiktok.\n\n"
        "🛍️ Shopee:\n"
        "   `/recommend <từ_khóa>` 🔍 - Tìm kiếm sản phẩm Shopee.\n"
        "   `/shopee <url_sản_phẩm>` ℹ️ - Tóm tắt về sản phẩm Shopee.\n\n"
        "☀️ Khám phá thêm:\n"
        "   `/weather <thành_phố>` ☀️ - Xem thời tiết hiện tại.\n\n"
        "🧹 Dọn dẹp:\n"
        "   `/clear` 🧹 - Xóa lịch sử trò chuyện.\n\n"
        "❓ Cần trợ giúp? `/help` 🙋‍♀️"
    )
    update.message.reply_text(help_text, parse_mode='Markdown')

# Leak Information
def leak_update(update: Update, context: CallbackContext):
    # Tạo thông báo về các cập nhật sắp tới cho Rita
    upcoming_features = (
        "🌟 Cảm ơn bạn đã quan tâm đến Rita! Với phiên bản sắp tới Rita v3.0, chúng tôi dự kiến sẽ mang đến một số cải tiến và tính năng mới:\n\n"
        "🧠 Về Model AI:\n"
        "• Nâng cao chất lượng trả lời của model AI, cung cấp câu trả lời chính xác hơn và có thể chèn link tham khảo.\n"
        "• Thêm khả năng tạo hình ảnh dựa trên mô tả của người dùng.\n\n"
        "🛠️ Về Tính năng mới:\n"
        "• Phân tích sản phẩm từ các link Shopee để đưa ra thông tin chi tiết.\n"
        "• Công cụ phân tích dữ liệu từ các trò chơi online, giúp bạn hiểu rõ hơn về cách chơi và chiến lược.\n"
        "• Đánh giá độ bảo mật của mật khẩu, đưa ra khuyến nghị cải thiện.\n\n"
        "📬 Một lần nữa cảm ơn bạn đã quan tâm đến Rita. Nếu bạn có thắc mắc hoặc ý tưởng nào, xin vui lòng liên hệ trực tiếp qua: [https://t.me/CterLQP](https://t.me/CterLQP).\n"
        "                                                      🙏 ~~Cảm ơn bạn~~"
    )

    # Gửi thông tin đã được định dạng
    update.message.reply_text(upcoming_features)


# Feedback
def handle_feedback(update, context):
    # Lấy thông tin người dùng từ tin nhắn.
    user = update.message.from_user
    user_name = user.first_name
    if user.last_name:
        user_name += ' ' + user.last_name

    # Lấy nội dung feedback, loại bỏ phần lệnh '/feedback '.
    feedback_text = update.message.text[10:]

    # Tạo thông điệp để lưu vào file.
    message_to_save = f'user: {user_name}, Feedback: {feedback_text}n'

    # Mở file (nếu file không tồn tại, Python sẽ tự tạo file) và ghi thông tin vào.
    with open('feedbacks.txt', 'a', encoding="utf-8") as file:
        file.write(message_to_save)

    # Gửi phản hồi lại cho người dùng.
    update.message.reply_text('Feedback của bạn đã được lưu lại. Cảm ơn bạn đã đóng góp!')

def clear_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id in chat_history:
        del chat_history[chat_id]
    update.message.reply_text("Lịch sử trò chuyện đã được xóa.")

# phản hồi user
def dynamic_typing_delay(message):
    # Calculate delay based on the length of the message
    words = len(message.split())
    typing_time_per_word = 0.5  # Average seconds it takes to 'type' a word
    return max(2, min(5, words * typing_time_per_word))
def handle_message(update: Update, context: CallbackContext):
    save_data_user(update, context)
    chat_id = update.message.chat_id
    user_message = str(update.message.text).lower()
    response = get_response(chat_id, user_message)
    delay = dynamic_typing_delay(response)
    send_typing(update, context, duration=delay)
    update.message.reply_text(response)

def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")

# Search Wiki
def wiki_command(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) == 0:
      update.message.reply_text("Thêm Keyword sau câu lệnh nhé. Ví dụ: /wiki Python.😒")
      return

    search_query = ' '.join(args)
    wikipedia.set_lang("vi")
    try:
      summary = wikipedia.summary(search_query, sentences=10)
      update.message.reply_text(summary)
    except wikipedia.exceptions.PageError:
      update.message.reply_text(f"Chắc là đúng từ khóa {search_query} không vậy??? 🤨")
    except wikipedia.exceptions.DisambiguationError as e:
      options = e.options
      update.message.reply_text(f"Một số trang có thể phù hợp: n" + "n".join(options[:5]) + "n...")
    except Exception as e:
      update.message.reply_text(f"Cái quần què, bị lỗi mịa ròi: {e}")
    pass

#Lưu thông tin người dùng
def save_data_user(update, context):
    log_file_path = 'user_data.txt'  # Đổi tên file và định dạng

    # Lấy thông tin từ update
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "UnknownUser"
    first_name = update.effective_user.first_name or ""
    last_name = update.effective_user.last_name or ""
    message_text = update.message.text
    timestamp = update.message.date.strftime('%Y-%m-%d %H:%M:%S')

    # Tạo một DataFrame từ dữ liệu
    new_data = pd.DataFrame({
        "Timestamp": [timestamp],
        "Chat ID": [chat_id],
        "Username": [username],
        "Full Name": [f"{first_name} {last_name}"],
        "Message": [message_text]
    })

    # Kiểm tra xem file đã tồn tại hay chưa
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0:
        # Nếu file tồn tại và không trống, đọc nội dung hiện tại và thêm dữ liệu mới
        existing_data = pd.read_csv(log_file_path, sep='\t', quotechar='"', escapechar='\\')
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        # Nếu file chưa tồn tại hoặc trống, dữ liệu mới là dữ liệu hiện tại
        updated_data = new_data

    # Ghi dữ liệu vào file TXT dưới dạng CSV
    updated_data.to_csv(log_file_path, index=False, sep='\t', quotechar='"', escapechar='\\')

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("wiki", wiki_command))
    dp.add_handler(CommandHandler("clear", clear_command))
    dp.add_handler(CommandHandler("search", Youtube_search))
    dp.add_handler(CommandHandler("weather", get_weather, pass_args=True))
    dp.add_handler(CommandHandler('feedback', handle_feedback))
    dp.add_handler(CommandHandler('leak', leak_update))
    dp.add_handler(CommandHandler("shopee", shopee))
    dp.add_handler(CommandHandler("download_ytb", download, pass_args=True))
    dp.add_handler(CommandHandler("analysis_ytb", analyze_video, pass_args=True))
    dp.add_handler(CommandHandler("download_tik", tiktok_dl, pass_args=True))
    dp.add_handler((CommandHandler("analysis_tik", analyze_tiktok)))
    dp.add_handler((CommandHandler('recommend', recommend_product, pass_args=True)))
    dp.add_handler(CommandHandler('file', send_document, pass_args=True)) # Tạm phong ấn
    dp.add_handler(CommandHandler('doc', display_documents)) # Tạm phong ấn
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()