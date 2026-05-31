'use client'

import { useState } from 'react'

interface TrackCardProps {
  id: number
  title: string
  artist: string
  coverUrl?: string
  duration?: number
  klickCount: number
  onPlay: (id: number) => void
  onKlick: (id: number) => void
}

export default function TrackCard({ id, title, artist, coverUrl, duration, klickCount, onPlay, onKlick }: TrackCardProps) {
  const [isHovered, setIsHovered] = useState(false)

  const formatDuration = (seconds?: number) => {
    if (!seconds) return '--:--'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition cursor-pointer"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-center gap-4">
        <div className="relative">
          {coverUrl ? (
            <img
              src={coverUrl}
              alt={title}
              className="w-16 h-16 rounded-lg object-cover"
            />
          ) : (
            <div className="w-16 h-16 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <span className="text-white text-2xl">🎵</span>
            </div>
          )}
          
          {isHovered && (
            <button
              onClick={() => onPlay(id)}
              className="absolute inset-0 bg-black bg-opacity-50 rounded-lg flex items-center justify-center"
            >
              <span className="text-white text-2xl">▶️</span>
            </button>
          )}
        </div>

        <div className="flex-1">
          <h3 className="font-semibold text-gray-800">{title}</h3>
          <p className="text-gray-600 text-sm">{artist}</p>
          <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
            <span>⏱️ {formatDuration(duration)}</span>
            <span>👏 {klickCount}</span>
          </div>
        </div>

        <button
          onClick={() => onKlick(id)}
          className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full hover:bg-purple-200 transition text-sm"
        >
          👏 Klick
        </button>
      </div>
    </div>
  )
}
