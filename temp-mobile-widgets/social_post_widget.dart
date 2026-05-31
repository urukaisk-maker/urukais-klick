import 'package:flutter/material.dart';

class SocialPostWidget extends StatelessWidget {
  final int id;
  final String user;
  final String content;
  final Map<String, dynamic>? track;
  final String? mood;
  final int reactions;
  final Function(int) onReact;

  const SocialPostWidget({
    super.key,
    required this.id,
    required this.user,
    required this.content,
    this.track,
    this.mood,
    required this.reactions,
    required this.onReact,
  });

  final Map<String, String> _moodEmojis = {
    'happy': '😊',
    'sad': '😢',
    'energetic': '⚡',
    'relaxed': '😌',
    'romantic': '💕',
    'focused': '🎯',
    'nostalgic': '📻',
    'adventurous': '🌍',
  };

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // User info
            Row(
              children: [
                CircleAvatar(
                  backgroundColor: const Color(0xFF6366F1),
                  child: Text(
                    user[0].toUpperCase(),
                    style: const TextStyle(color: Colors.white),
                  ),
                ),
                const SizedBox(width: 12),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      user,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    if (mood != null)
                      Text(
                        _moodEmojis[mood] ?? '🎵',
                        style: const TextStyle(fontSize: 20),
                      ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 12),
            
            // Content
            Text(content),
            
            // Track attachment
            if (track != null) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 48,
                      height: 48,
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF6366F1), Color(0xFF9333EA)],
                        ),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: const Icon(Icons.music_note, color: Colors.white),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            track!['title'],
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          Text(
                            track!['artist'],
                            style: TextStyle(color: Colors.grey[600]),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
            
            const SizedBox(height: 12),
            
            // Reactions
            Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.thumb_up_outlined),
                  onPressed: () => onReact(id),
                ),
                Text('$reactions'),
                const SizedBox(width: 16),
                IconButton(
                  icon: const Icon(Icons.comment_outlined),
                  onPressed: () {},
                ),
                const Text('Responder'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
