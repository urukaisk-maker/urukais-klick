import 'package:flutter/material.dart';
import 'package:urukais_klick/widgets/track_card_widget.dart';

class DiscoveryScreen extends StatefulWidget {
  const DiscoveryScreen({super.key});

  @override
  State<DiscoveryScreen> createState() => _DiscoveryScreenState();
}

class _DiscoveryScreenState extends State<DiscoveryScreen> {
  String _filter = 'klicks';

  final List<Map<String, dynamic>> _tracks = [
    {
      'id': 1,
      'title': 'Ecos de la Noche',
      'artist': 'Luna Solitaria',
      'duration': 245,
      'klick_count': 42,
    },
    {
      'id': 2,
      'title': 'Ritmo Urbano',
      'artist': 'Callejero Beats',
      'duration': 198,
      'klick_count': 38,
    },
    {
      'id': 3,
      'title': 'Melancolía Azul',
      'artist': 'Sombra Eterna',
      'duration': 312,
      'klick_count': 55,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Descubrir'),
        backgroundColor: const Color(0xFF6366F1),
      ),
      body: Column(
        children: [
          // Filter tabs
          Container(
            padding: const EdgeInsets.symmetric(vertical: 12),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildFilterChip('klicks', '🎯 Para Ti'),
                _buildFilterChip('trending', '🔥 Trending'),
                _buildFilterChip('discovery', '🌍 Descubrir'),
              ],
            ),
          ),
          const Divider(),
          // Track list
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _tracks.length,
              itemBuilder: (context, index) {
                final track = _tracks[index];
                return TrackCardWidget(
                  id: track['id'],
                  title: track['title'],
                  artist: track['artist'],
                  duration: track['duration'],
                  klickCount: track['klick_count'],
                  onPlay: (id) => _handlePlayTrack(id),
                  onKlick: (id) => _handleKlickTrack(id),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterChip(String value, String label) {
    final isSelected = _filter == value;
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) {
        setState(() => _filter = value);
      },
      selectedColor: const Color(0xFF6366F1),
      backgroundColor: Colors.grey[200],
    );
  }

  void _handlePlayTrack(int id) {
    // Implementar reproducción
    print('Reproduciendo pista: $id');
  }

  void _handleKlickTrack(int id) {
    // Implementar Klick
    print('Klick enviado para pista: $id');
  }
}
