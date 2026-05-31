'use client'

import { useState } from 'react'
import SocialPost from './SocialPost'

interface Post {
  id: number
  user: string
  content: string
  track?: {
    title: string
    artist: string
    cover_url?: string
  }
  mood?: string
  reactions: number
}

interface SocialWallProps {
  posts: Post[]
  onReact: (postId: number) => void
  onCreatePost: (content: string, trackId?: number, mood?: string) => void
}

export default function SocialWall({ posts, onReact, onCreatePost }: SocialWallProps) {
  const [newPost, setNewPost] = useState('')
  const [showCreatePost, setShowCreatePost] = useState(false)

  const handleSubmit = () => {
    if (newPost.trim()) {
      onCreatePost(newPost)
      setNewPost('')
      setShowCreatePost(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <button
          onClick={() => setShowCreatePost(!showCreatePost)}
          className="w-full text-left text-gray-600 hover:text-gray-800 transition"
        >
          ¿Qué estás sintiendo ahora? 🎵
        </button>

        {showCreatePost && (
          <div className="mt-4">
            <textarea
              value={newPost}
              onChange={(e) => setNewPost(e.target.value)}
              placeholder="Comparte tu estado de ánimo con la comunidad..."
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              rows={3}
            />
            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => setShowCreatePost(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancelar
              </button>
              <button
                onClick={handleSubmit}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
              >
                Publicar
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="space-y-4">
        {posts.map((post) => (
          <SocialPost
            key={post.id}
            id={post.id}
            user={post.user}
            content={post.content}
            track={post.track}
            mood={post.mood}
            reactions={post.reactions}
            onReact={onReact}
          />
        ))}
      </div>

      {posts.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600 text-lg">No hay publicaciones aún</p>
          <p className="text-gray-400 text-sm mt-2">Sé el primero en compartir con la comunidad</p>
        </div>
      )}
    </div>
  )
}
