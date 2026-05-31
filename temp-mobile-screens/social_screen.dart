import 'package:flutter/material.dart';
import 'package:urukais_klick/widgets/social_post_widget.dart';

class SocialScreen extends StatefulWidget {
  const SocialScreen({super.key});

  @override
  State<SocialScreen> createState() => _SocialScreenState();
}

class _SocialScreenState extends State<SocialScreen> {
  final List<Map<String, dynamic>> _posts = [
    {
      'id': 1,
      'user': 'Melómano',
      'content': 'Hoy me siento nostálgico, escuchando viejos clásicos 📻',
      'mood': 'nostalgic',
      'reactions': 12,
    },
    {
      'id': 2,
      'user': 'MusicLover',
      'content': '¡Acabo de descubrir a este artista increíble! 🎵',
      'track': {
        'title': 'Ecos de la Noche',
        'artist': 'Luna Solitaria',
      },
      'reactions': 8,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Muro Social'),
        backgroundColor: const Color(0xFF6366F1),
      ),
      body: Column(
        children: [
          // Create post input
          Container(
            padding: const EdgeInsets.all(16),
            child: TextField(
              decoration: InputDecoration(
                hintText: '¿Qué estás sintiendo ahora? 🎵',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                ),
                filled: true,
                fillColor: Colors.grey[100],
              ),
            ),
          ),
          const Divider(),
          // Posts list
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _posts.length,
              itemBuilder: (context, index) {
                final post = _posts[index];
                return SocialPostWidget(
                  id: post['id'],
                  user: post['user'],
                  content: post['content'],
                  track: post['track'],
                  mood: post['mood'],
                  reactions: post['reactions'],
                  onReact: (id) => _handleReact(id),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showCreatePostDialog(),
        backgroundColor: const Color(0xFF6366F1),
        child: const Icon(Icons.add),
      ),
    );
  }

  void _handleReact(int postId) {
    print('Reacción enviada para post: $postId');
  }

  void _showCreatePostDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Crear Publicación'),
        content: TextField(
          maxLines: 4,
          decoration: const InputDecoration(
            hintText: 'Comparte tu estado de ánimo...',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              print('Post creado');
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF6366F1),
            ),
            child: const Text('Publicar'),
          ),
        ],
      ),
    );
  }
}
