# AI Image Generator

![App Screenshot](./public/images/screenshot.png)
*Screenshot of the AI Image Generator application*

## What is this?
This is a web application that generates high-quality anime-style images using OpenAI's DALL-E 3 API. Users can input text descriptions, and the application will generate two different variations of anime-style images based on the provided prompt.

## Features
- Generate two anime-style images simultaneously
- High-quality image output using DALL-E 3
- Real-time loading states and error handling
- Responsive design for both desktop and mobile
- User-friendly interface with input suggestions

## How to Use
1. Enter a detailed description of the anime image you want to generate
2. Include details about:
   - Character appearance (hair, eyes, expression)
   - Clothing and accessories
   - Pose and action
   - Background and environment
   - Lighting and atmosphere
3. Click the "Generate" button
4. Wait for both images to be generated
5. Images will be displayed in the preview area

### Example Result
![Example Generated Image](./public/images/example.png)
*Example of a generated image using the prompt: "hatsune miku wearing swimming suit and holding a birthday cake, with big smile on her face in brightly sky background"*

Example prompt:

## Running Locally

1. **Clone the repository**
```bash
git clone [repository-url]
cd [project-name]
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
Create a `.env.local` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key
```

4. **Get OpenAI API Key**
- Visit https://platform.openai.com/api-keys
- Sign up or log in to your OpenAI account
- Create a new API key
- Copy and paste it into your `.env.local` file

5. **Start the development server**
```bash
npm run dev
```

6. **Open the application**
Visit `http://localhost:3000` in your browser

## Requirements
- Node.js 18.17.0 or later
- OpenAI API key with DALL-E access
- Modern web browser

## Credit
This app is created by cursor

---

For any issues or questions, please open an issue in the repository.