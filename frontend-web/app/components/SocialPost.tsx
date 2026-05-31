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
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold">
          {user.charAt(0).toUpperCase()}
        </div>

        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="font-semibold">{user}</span>
            {mood && (
              <span className="text-2xl">{moodEmojis[mood] || '🎵'}</span>
            )}
          </div>

          <p className="text-gray-800 mb-4">{content}</p>

          {track && (
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <div className="flex items-center gap-4">
                {track.coverUrl ? (
                  <img
                    src={track.coverUrl}
                    alt={track.title}
                    className="w-12 h-12 rounded object-cover"
                  />
                ) : (
                  <div className="w-12 h-12 rounded bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                    <span className="text-white">🎵</span>
                  </div>
                )}
                <div>
                  <p className="font-semibold">{track.title}</p>
                  <p className="text-gray-600 text-sm">{track.artist}</p>
                </div>
              </div>
            </div>
          )}

          <div className="flex items-center gap-4">
            <button
              onClick={() => onReact(id)}
              className="text-gray-600 hover:text-purple-600 transition"
            >
              👏 {reactions}
            </button>
            <button
              onClick={() => setShowReactions(!showReactions)}
              className="text-gray-600 hover:text-indigo-600 transition"
            >
              💬 Responder
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
