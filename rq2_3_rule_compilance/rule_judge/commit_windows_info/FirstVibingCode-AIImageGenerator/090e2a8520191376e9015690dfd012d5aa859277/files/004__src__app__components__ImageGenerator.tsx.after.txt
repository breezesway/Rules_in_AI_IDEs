'use client'

import { useState } from 'react'
import Image from 'next/image'

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState('')
  const [images, setImages] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const generateImages = async () => {
    if (!prompt) return
    
    setLoading(true)
    setError('')
    try {
      // 生成第一张图片
      const response = await fetch('/api/openai/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          prompt: `anime style artwork, highly detailed, masterpiece quality, ${prompt}, cute anime character, soft pastel colors, gentle expression, detailed eyes with sparkles`
        })
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'Error: ' + response.status)
      }

      if (data.error) {
        throw new Error(data.error)
      }

      setImages([data.imageUrl])

      // 生成第二张图片
      const secondResponse = await fetch('/api/openai/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          prompt: `anime style artwork, highly detailed, masterpiece quality, ${prompt}, dynamic anime scene, vibrant colors, dramatic lighting`
        })
      })

      const secondData = await secondResponse.json()
      
      if (!secondResponse.ok) {
        throw new Error(secondData.error || 'Error: ' + secondResponse.status)
      }

      setImages([data.imageUrl, secondData.imageUrl])
    } catch (error) {
      console.error('Error details:', error)
      setError(error instanceof Error ? error.message : '生成图片时出错')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {error && (
        <div className="bg-red-50 text-red-500 p-4 rounded-xl">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[0, 1].map((index) => (
          <div 
            key={index} 
            className="aspect-square rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden flex items-center justify-center transition-shadow hover:shadow-md"
          >
            {images[index] ? (
              <Image 
                src={images[index]} 
                alt={`Generated image ${index + 1}`} 
                width={1024} 
                height={1024} 
                className="w-full h-full object-cover"
                priority
              />
            ) : (
              <div className="text-gray-400 font-light flex flex-col items-center">
                <p>waiting to generate image...</p>
                {loading && index >= images.length && (
                  <div className="mt-2 w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"/>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="space-y-4">
        <div className="text-sm text-gray-600">
          提示詞：描述角色的外觀、表情、姿勢、服裝和背景等細節
        </div>
        <div className="flex gap-4">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="描述您想要的动漫风格图片..."
            className="flex-1 px-6 py-4 rounded-xl border border-gray-200 bg-white shadow-sm 
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                     placeholder-gray-400 text-gray-600"
          />
          <button
            onClick={generateImages}
            disabled={loading || !prompt}
            className="px-8 py-4 bg-[#1a365d] text-white rounded-xl shadow-sm
                     hover:bg-[#2d4a7c] transition-colors duration-200
                     disabled:bg-gray-300 disabled:cursor-not-allowed
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            {loading ? (
              <div className="flex items-center space-x-2">
                <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"/>
                <span>生成中...</span>
              </div>
            ) : (
              '生成图片'
            )}
          </button>
        </div>
      </div>
    </div>
  )
} 