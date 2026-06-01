'use client'

import { useState, useRef, useEffect } from 'react'

interface AudioPlayerProps {
  audioUrl: string
  title: string
  artist?: string
  coverUrl?: string
  onKlick?: () => void
}

export default function AudioPlayer({ audioUrl, title, artist, coverUrl, onKlick }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime)
    const handleLoadedMetadata = () => setDuration(audio.duration)
    const handleEnded = () => setIsPlaying(false)

    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('ended', handleEnded)

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('ended', handleEnded)
    }
  }, [])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current
    if (!audio) return

    const newTime = parseFloat(e.target.value)
    audio.currentTime = newTime
    setCurrentTime(newTime)
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current
    if (!audio) return

    const newVolume = parseFloat(e.target.value)
    audio.volume = newVolume
    setVolume(newVolume)
  }

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
  }

  return (
    <div className="glass-effect rounded-2xl p-6 max-w-4xl mx-auto backdrop-blur-xl">
      <audio ref={audioRef} src={audioUrl} />
      
      <div className="flex items-center gap-4 mb-4">
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
        <div className="flex-1">
          <h3 className="font-bold text-white text-xl">{title}</h3>
          {artist && <p className="text-white/70 text-sm">{artist}</p>}
        </div>
      </div>

      <div className="mb-4">
        <input
          type="range"
          min="0"
          max={duration || 0}
          value={currentTime}
          onChange={handleSeek}
          className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer accent-white"
        />
        <div className="flex justify-between text-sm text-white/70 mt-1">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={togglePlay}
            className="btn-gradient text-white px-8 py-3 rounded-full font-semibold hover:scale-105 transition-transform"
          >
            {isPlaying ? '⏸️ Pausar' : '▶️ Reproducir'}
          </button>
          
          {onKlick && (
            <button
              onClick={onKlick}
              className="bg-white/20 text-white px-6 py-3 rounded-full hover:bg-white/30 transition font-semibold border border-white/20 backdrop-blur-sm"
            >
              👏 Klick
            </button>
          )}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xl text-white/80">🔊</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={handleVolumeChange}
            className="w-32 h-2 bg-white/20 rounded-lg appearance-none cursor-pointer accent-white"
          />
        </div>
      </div>
    </div>
  )
}
