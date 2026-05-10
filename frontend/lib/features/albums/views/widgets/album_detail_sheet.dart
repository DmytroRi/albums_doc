import 'package:albums_frontend/generated_api/lib/model/models.dart';
import 'package:flutter/material.dart';

class AlbumDetailSheet extends StatelessWidget {
  const AlbumDetailSheet({super.key, required this.album});

  final AlbumRead album;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: SingleChildScrollView(
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(album.title, style: Theme.of(context).textTheme.headlineSmall),
          Text('Artists: ${album.artists.join(', ')}'),
          Text('Year: ${album.releaseYear}'),
          Text('Grade: ${album.grade.toStringAsFixed(1)}'),
          Text('Producers: ${album.producers.join(', ')}'),
          Text('Genres: ${album.genres.join(', ')}'),
          Text('Moods: ${album.moods.join(', ')}'),
          const SizedBox(height: 12),
          const Text('Tracks:'),
          ...album.tracks.map((t) => Text('${t.trackOrder}. ${t.title} (${t.durationSeconds}s)')),
        ]),
      ),
    );
  }
}
