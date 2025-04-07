
# AI Chatbot with Image Processing

<p align="center">
  <img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="400" alt="Laravel Logo">
</p>

## Project Features

- **AI-Powered Chat**: Conversational interface with natural language processing
- **Image Processing**: Extract text and generate HTML layouts from images
- **Multi-Modal Input**: Support for both text and image inputs
- **Real-Time Processing**: Fast response times with loading indicators
- **Modern UI**: Clean, responsive interface with dark/light mode support

## Technologies Used

- **Backend**: Laravel PHP framework
- **Frontend**: Vue.js with Tailwind CSS
- **AI Services**: 
  - PaddleOCR for text extraction
  - Stable Diffusion for image generation
  - Segment Anything (SAM) for image segmentation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/khelangit/ai-chatbot.git
cd ai-chatbot
```
2. Install dependencies:
```bash
composer install
npm install
 ```

3. Configure environment:
```bash
cp .env.example .env
php artisan key:generate
 ```

4. Run the application:
```bash
php artisan serve
npm run dev
 ```

## Configuration
'''ini:

AI_API_ENDPOINT=http://localhost:8001
OCR_MODEL_PATH=/path/to/ocr/model
IMAGE_PROCESSING_ENABLED=true 
'''

## License
This project is open-sourced software licensed under the MIT license.
Key improvements:
1. Removed Laravel-specific content not relevant to your project
2. Added clear project features and technologies
3. Included practical installation instructions
4. Added configuration section for AI services
5. Kept the professional formatting and MIT license

The README now better represents your actual project while maintaining a professional appearance. Would you like me to make any additional adjustments?
