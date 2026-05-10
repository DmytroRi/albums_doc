import 'package:albums_frontend/features/albums/bloc/albums_bloc.dart';
import 'package:albums_frontend/features/albums/bloc/albums_event.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AlbumCreateDialog extends StatelessWidget {
  const AlbumCreateDialog({super.key});

  @override
  Widget build(BuildContext context) {
    final title = TextEditingController();
    final year = TextEditingController();
    final grade = TextEditingController();
    final artists = TextEditingController();
    final producers = TextEditingController();
    final genres = TextEditingController();
    final moods = TextEditingController();
    final tracks = TextEditingController();

    List<String> splitCsv(String value) => value.split(',').map((e) => e.trim()).where((e) => e.isNotEmpty).toList();

    return AlertDialog(
      title: const Text('Create album'),
      content: SingleChildScrollView(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          TextField(controller: title, decoration: const InputDecoration(labelText: 'Title')),
          TextField(controller: year, decoration: const InputDecoration(labelText: 'Year')),
          TextField(controller: grade, decoration: const InputDecoration(labelText: 'Grade')),
          TextField(controller: artists, decoration: const InputDecoration(labelText: 'Artists (comma separated)')),
          TextField(controller: producers, decoration: const InputDecoration(labelText: 'Producers (comma separated)')),
          TextField(controller: genres, decoration: const InputDecoration(labelText: 'Genres (comma separated)')),
          TextField(controller: moods, decoration: const InputDecoration(labelText: 'Moods (comma separated)')),
          TextField(controller: tracks, decoration: const InputDecoration(labelText: 'Tracks format: name|seconds,name|seconds')),
        ]),
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
        FilledButton(
          onPressed: () {
            final trackValues = splitCsv(tracks.text);
            final payload = {
              'title': title.text,
              'release_year': int.parse(year.text),
              'grade': double.parse(grade.text),
              'artists': splitCsv(artists.text),
              'producers': splitCsv(producers.text),
              'genres': splitCsv(genres.text),
              'moods': splitCsv(moods.text),
              'tracks': trackValues.asMap().entries.map((entry) {
                final parts = entry.value.split('|');
                return {
                  'title': parts.first.trim(),
                  'duration_seconds': int.parse(parts.last.trim()),
                  'track_order': entry.key + 1,
                };
              }).toList(),
            };
            context.read<AlbumsBloc>().add(AlbumCreateSubmitted(payload));
            Navigator.pop(context);
          },
          child: const Text('Create'),
        ),
      ],
    );
  }
}
