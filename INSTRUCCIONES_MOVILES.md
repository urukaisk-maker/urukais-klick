# Instrucciones para instalar archivos del frontend móvil

Los archivos del frontend móvil están en el directorio `temp-mobile-screens/` y `temp-mobile-widgets/` porque el directorio original está protegido por `.gitignore`.

## Pasos para mover los archivos:

1. **Crear directorios necesarios:**
```powershell
New-Item -ItemType Directory -Path "frontend-mobile/lib/screens" -Force
New-Item -ItemType Directory -Path "frontend-mobile/lib/widgets" -Force
```

2. **Mover archivos de screens:**
```powershell
Copy-Item "temp-mobile-screens/login_screen.dart" "frontend-mobile/lib/screens/login_screen.dart"
Copy-Item "temp-mobile-screens/register_screen.dart" "frontend-mobile/lib/screens/register_screen.dart"
Copy-Item "temp-mobile-screens/home_screen.dart" "frontend-mobile/lib/screens/home_screen.dart"
Copy-Item "temp-mobile-screens/discovery_screen.dart" "frontend-mobile/lib/screens/discovery_screen.dart"
Copy-Item "temp-mobile-screens/social_screen.dart" "frontend-mobile/lib/screens/social_screen.dart"
Copy-Item "temp-mobile-screens/live_screen.dart" "frontend-mobile/lib/screens/live_screen.dart"
```

3. **Mover archivos de widgets:**
```powershell
Copy-Item "temp-mobile-widgets/track_card_widget.dart" "frontend-mobile/lib/widgets/track_card_widget.dart"
Copy-Item "temp-mobile-widgets/social_post_widget.dart" "frontend-mobile/lib/widgets/social_post_widget.dart"
Copy-Item "temp-mobile-widgets/live_room_widget.dart" "frontend-mobile/lib/widgets/live_room_widget.dart"
Copy-Item "temp-mobile-widgets/audio_player_widget.dart" "frontend-mobile/lib/widgets/audio_player_widget.dart"
```

4. **Actualizar pubspec.yaml:**
Agregar las siguientes dependencias:
```yaml
dependencies:
  flutter:
    sdk: flutter
  just_audio: ^0.9.36
  http: ^1.1.0
```

5. **Actualizar main.dart:**
Reemplazar el contenido de `frontend-mobile/lib/main.dart` con:
```dart
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
```

6. **Instalar dependencias y ejecutar:**
```powershell
cd frontend-mobile
flutter pub get
flutter run
```

## Archivos creados:

### Screens:
- `login_screen.dart` - Pantalla de login
- `register_screen.dart` - Registro con ruleta de estados de ánimo
- `home_screen.dart` - Pantalla principal con navegación
- `discovery_screen.dart` - Feed de descubrimiento
- `social_screen.dart` - Muro social
- `live_screen.dart` - Salas en directo

### Widgets:
- `track_card_widget.dart` - Tarjeta de pista
- `social_post_widget.dart` - Post del muro social
- `live_room_widget.dart` - Tarjeta de sala en vivo
- `audio_player_widget.dart` - Reproductor de audio
