'use client'

interface LiveRoomCardProps {
  id: number
  title: string
  host: string
  listeners: number
  isLive: boolean
  onJoin: (roomId: number) => void
}

export default function LiveRoomCard({ id, title, host, listeners, isLive, onJoin }: LiveRoomCardProps) {
  return (
    <div className="glass-effect rounded-2xl p-6 card-hover cursor-pointer border-2 border-white/20 hover:border-white/40">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-red-500 to-pink-600 flex items-center justify-center text-white font-bold text-xl shadow-lg">
              {host.charAt(0).toUpperCase()}
            </div>
            {isLive && (
              <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-red-500 rounded-full border-2 border-white animate-pulse shadow-lg" />
            )}
          </div>
          <div>
            <h3 className="font-bold text-white text-lg">{title}</h3>
            <p className="text-white/70 text-sm">por {host}</p>
          </div>
        </div>

        {isLive && (
          <span className="bg-red-500/20 text-red-300 px-4 py-1 rounded-full text-sm font-semibold border border-red-500/30 backdrop-blur-sm">
            🔴 EN VIVO
          </span>
        )}
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-white/80">
          <span className="text-xl">👥</span>
          <span className="font-medium">{listeners} escuchando</span>
        </div>

        <button
          onClick={() => onJoin(id)}
          className="btn-gradient text-white px-6 py-2 rounded-full font-semibold hover:scale-105 transition-transform"
        >
          Unirse
        </button>
      </div>
    </div>
  )
}
