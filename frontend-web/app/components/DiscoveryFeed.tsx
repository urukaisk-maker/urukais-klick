'use client'

import { useState } from 'react'
import TrackCard from './TrackCard'

interface Track {
  id: number
  title: string
  artist: string
  cover_url?: string
  duration?: number
  klick_count: number
}

interface DiscoveryFeedProps {
  tracks: Track[]
  onPlayTrack: (id: number) => void
  onKlickTrack: (id: number) => void
}

export default function DiscoveryFeed({ tracks, onPlayTrack, onKlickTrack }: DiscoveryFeedProps) {
  const [filter, setFilter] = useState<'klicks' | 'trending' | 'discovery'>('klicks')

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => setFilter('klicks')}
          className={`px-4 py-2 rounded-full transition ${
            filter === 'klicks'
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          🎯 Para Ti
        </button>
        <button
          onClick={() => setFilter('trending')}
          className={`px-4 py-2 rounded-full transition ${
            filter === 'trending'
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          🔥 Trending
        </button>
        <button
          onClick={() => setFilter('discovery')}
          className={`px-4 py-2 rounded-full transition ${
            filter === 'discovery'
              ? 'bg-indigo-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          🌍 Descubrir
        </button>
      </div>

      <div className="space-y-4">
        {tracks.map((track) => (
          <TrackCard
            key={track.id}
            id={track.id}
            title={track.title}
            artist={track.artist}
            coverUrl={track.cover_url}
            duration={track.duration}
            klickCount={track.klick_count}
            onPlay={onPlayTrack}
            onKlick={onKlickTrack}
          />
        ))}
      </div>

      {tracks.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg">No hay pistas disponibles</p>
          <p className="text-gray-400 text-sm mt-2">Vuelve más tarde para descubrir nueva música</p>
        </div>
      )}
    </div>
  )
}
