'use client'

import { useState } from 'react'

interface SocialPostProps {
  id: number
  user: string
  content: string
  track?: {
    title: string
    artist: string
    coverUrl?: string
  }
  mood?: string
  reactions: number
  onReact: (postId: number) => void
}

export default function SocialPost({ id, user, content, track, mood, reactions, onReact }: SocialPostProps) {
  const [showReactions, setShowReactions] = useState(false)

  const moodEmojis: Record<string, string> = {
    happy: '😊',
    sad: '😢',
    energetic: '⚡',
    relaxed: '😌',
    romantic: '💕',
    focused: '🎯',
    nostalgic: '📻',
    adventurous: '🌍',
  }

  return (
    <div className="glass-effect rounded-2xl p-6 mb-4 card-hover">
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 rounded-full btn-gradient flex items-center justify-center text-white font-bold text-xl shadow-lg">
          {user.charAt(0).toUpperCase()}
        </div>

        <div className="flex-1">
          <div className="flex items-center gap-2 mb-3">
            <span className="font-bold text-white text-lg">{user}</span>
            {mood && (
              <span className="text-2xl">{moodEmojis[mood] || '🎵'}</span>
            )}
          </div>

          <p className="text-white/90 mb-4 text-lg">{content}</p>

          {track && (
            <div className="bg-white/10 rounded-xl p-4 mb-4 backdrop-blur-sm border border-white/20">
              <div className="flex items-center gap-4">
                {track.coverUrl ? (
                  <img
                    src={track.coverUrl}
                    alt={track.title}
                    className="w-14 h-14 rounded-xl object-cover shadow-md"
                  />
                ) : (
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-md">
                    <span className="text-white text-xl">🎵</span>
                  </div>
                )}
                <div>
                  <p className="font-semibold text-white">{track.title}</p>
                  <p className="text-white/70 text-sm">{track.artist}</p>
                </div>
              </div>
            </div>
          )}

          <div className="flex items-center gap-6">
            <button
              onClick={() => onReact(id)}
              className="text-white/80 hover:text-white transition flex items-center gap-2 hover:scale-105 transform"
            >
              👏 <span className="font-semibold">{reactions}</span>
            </button>
            <button
              onClick={() => setShowReactions(!showReactions)}
              className="text-white/80 hover:text-white transition flex items-center gap-2 hover:scale-105 transform"
            >
              💬 <span className="font-semibold">Responder</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
