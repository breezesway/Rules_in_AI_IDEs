import { NextResponse } from 'next/server'
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(req: Request) {
  if (!process.env.OPENAI_API_KEY) {
    console.error('OPENAI_API_KEY is not set')
    return NextResponse.json(
      { error: 'OpenAI API key is not configured' },
      { status: 500 }
    )
  }

  try {
    const { prompt } = await req.json()
    
    if (!prompt) {
      return NextResponse.json(
        { error: 'Prompt is required' },
        { status: 400 }
      )
    }

    console.log('Generating image with prompt:', prompt)

    // 优化动漫风格的提示词
    const enhancedPrompt = `Create a high-quality anime illustration in the style of modern Japanese animation:
    ${prompt}
    Art style specifications:
    - Vibrant and rich colors
    - Crisp, clean lines
    - Detailed anime eyes with light reflections and sparkles
    - Smooth gradients and shading
    - Detailed hair with individual strands and highlights
    - Precise facial features in anime style
    - High contrast lighting with soft shadows
    - Detailed clothing with proper folds and textures
    - Background with bokeh effects and atmospheric lighting
    - Anime-style composition and proportions
    The image should have the quality level of professional anime artwork, with attention to detail and polish similar to high-budget anime productions.`

    const response = await openai.images.generate({
      model: "dall-e-3",
      prompt: enhancedPrompt,
      n: 1,
      size: "1024x1024",
      quality: "hd",
      style: "vivid" // 使用 vivid 风格以获得更鲜艳的颜色
    })

    console.log('OpenAI response:', response)

    if (!response.data?.[0]?.url) {
      throw new Error('No image URL in response')
    }

    return NextResponse.json({ 
      imageUrl: response.data[0].url,
      created: response.created
    })
  } catch (error: any) {
    console.error('Detailed error:', error.response || error)
    
    // 返回更详细的错误信息
    return NextResponse.json({
      error: error.message || 'Failed to generate image',
      details: error.response?.data || error
    }, { 
      status: error.status || 500 
    })
  }
} 