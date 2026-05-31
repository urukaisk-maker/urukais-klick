import 'package:flutter/material.dart';
import 'package:urukais_klick/widgets/live_room_widget.dart';

class LiveScreen extends StatefulWidget {
  const LiveScreen({super.key});

  @override
  State<LiveScreen> createState() => _LiveScreenState();
}

class _LiveScreenState extends State<LiveScreen> {
  final List<Map<String, dynamic>> _rooms = [
    {
      'id': 1,
      'title': 'Jazz Session Nocturna',
      'host': 'SaxMaster',
      'current_listeners': 24,
      'is_active': true,
    },
    {
      'id': 2,
      'title': 'Indie Discovery Hour',
      'host': 'CuradorMusical',
      'current_listeners': 18,
      'is_active': true,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Salas en Directo'),
        backgroundColor: const Color(0xFF6366F1),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => _showCreateRoomDialog(),
          ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _rooms.length,
        itemBuilder: (context, index) {
          final room = _rooms[index];
          return LiveRoomWidget(
            id: room['id'],
            title: room['title'],
            host: room['host'],
            listeners: room['current_listeners'],
            isLive: room['is_active'],
            onJoin: (id) => _handleJoinRoom(id),
          );
        },
      ),
    );
  }

  void _handleJoinRoom(int roomId) {
    print('Uniéndose a sala: $roomId');
  }

  void _showCreateRoomDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Crear Nueva Sala'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              decoration: const InputDecoration(
                labelText: 'Título de la sala',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(
                labelText: 'Descripción (opcional)',
                border: OutlineInputBorder(),
              ),
              maxLines: 2,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              print('Sala creada');
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF6366F1),
            ),
            child: const Text('Crear'),
          ),
        ],
      ),
    );
  }
}
