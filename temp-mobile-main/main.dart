import 'package:flutter/material.dart';
import 'package:urukais_klick/screens/login_screen.dart';

void main() {
  runApp(const UrukaisKlickApp());
}

class UrukaisKlickApp extends StatelessWidget {
  const UrukaisKlickApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Urukais Klick',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}
