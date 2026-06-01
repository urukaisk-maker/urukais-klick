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
      className="glass-effect rounded-2xl p-5 card-hover cursor-pointer"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-center gap-4">
        <div className="relative">
          {coverUrl ? (
            <img
              src={coverUrl}
              alt={title}
              className="w-20 h-20 rounded-2xl object-cover shadow-lg"
            />
          ) : (
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
              <span className="text-white text-3xl">🎵</span>
            </div>
          )}
          
          {isHovered && (
            <button
              onClick={() => onPlay(id)}
              className="absolute inset-0 bg-black/60 rounded-2xl flex items-center justify-center backdrop-blur-sm transition-all duration-300"
            >
              <span className="text-white text-3xl">▶️</span>
            </button>
          )}
        </div>

        <div className="flex-1">
          <h3 className="font-bold text-white text-lg">{title}</h3>
          <p className="text-white/70 text-sm">{artist}</p>
          <div className="flex items-center gap-4 mt-2 text-sm text-white/60">
            <span>⏱️ {formatDuration(duration)}</span>
            <span>👏 {klickCount}</span>
          </div>
        </div>

        <button
          onClick={() => onKlick(id)}
          className="btn-gradient text-white px-4 py-2 rounded-full text-sm font-semibold hover:scale-105 transition-transform"
        >
          👏 Klick
        </button>
      </div>
    </div>
  )
}
