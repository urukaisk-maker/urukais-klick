import 'package:flutter/material.dart';

class LiveRoomWidget extends StatelessWidget {
  final int id;
  final String title;
  final String host;
  final int listeners;
  final bool isLive;
  final Function(int) onJoin;

  const LiveRoomWidget({
    super.key,
    required this.id,
    required this.title,
    required this.host,
    required this.listeners,
    required this.isLive,
    required this.onJoin,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Stack(
                  children: [
                    CircleAvatar(
                      backgroundColor: const Color(0xFFEF4444),
                      child: Text(
                        host[0].toUpperCase(),
                        style: const TextStyle(color: Colors.white),
                      ),
                    ),
                    if (isLive)
                      Positioned(
                        bottom: 0,
                        right: 0,
                        child: Container(
                          width: 16,
                          height: 16,
                          decoration: const BoxDecoration(
                            color: Colors.red,
                            shape: BoxShape.circle,
                          ),
                        ),
                      ),
                  ],
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                      Text(
                        'por $host',
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    ],
                  ),
                ),
                if (isLive)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.red[100],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      '🔴 EN VIVO',
                      style: TextStyle(
                        color: Colors.red,
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            
            // Footer
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const Icon(Icons.people, size: 20),
                    const SizedBox(width: 4),
                    Text('$listeners escuchando'),
                  ],
                ),
                ElevatedButton(
                  onPressed: () => onJoin(id),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF6366F1),
                  ),
                  child: const Text('Unirse'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
