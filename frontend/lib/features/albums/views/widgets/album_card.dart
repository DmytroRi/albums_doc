import 'package:albums_frontend/generated_api/lib/model/models.dart';
import 'package:flutter/material.dart';

class AlbumCard extends StatelessWidget {
  const AlbumCard({super.key, required this.album, required this.onTap});

  final AlbumSummary album;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        onTap: onTap,
        title: Text(album.title),
        subtitle: Text('${album.artists.join(', ')} • ${album.releaseYear}'),
        trailing: Text(album.grade.toStringAsFixed(1)),
      ),
    );
  }
}
