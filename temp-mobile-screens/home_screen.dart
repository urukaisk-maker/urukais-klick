import 'package:flutter/material.dart';
import 'package:urukais_klick/screens/discovery_screen.dart';
import 'package:urukais_klick/screens/social_screen.dart';
import 'package:urukais_klick/screens/live_screen.dart';
import 'package:urukais_klick/widgets/audio_player_widget.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;
  final List<Widget> _screens = [
    const DiscoveryScreen(),
    const SocialScreen(),
    const LiveScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.explore),
            label: 'Descubrir',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Social',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.radio),
            label: 'Live',
          ),
        ],
      ),
    );
  }
}
