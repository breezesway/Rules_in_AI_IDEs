'use client'

import { useState } from 'react'
import ImageGenerator from './components/ImageGenerator'

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <nav className="bg-[#1a365d] shadow-lg p-4 fixed top-0 left-0 right-0 z-10">
        <div className="max-w-6xl mx-auto flex justify-end space-x-6 text-gray-100">
          <a href="/" className="hover:text-white transition-colors">Home</a>
          <a href="/about" className="hover:text-white transition-colors">About</a>
        </div>
      </nav>
      
      <div className="max-w-6xl mx-auto pt-24 px-4">
        <ImageGenerator />
      </div>
    </main>
  )
}
