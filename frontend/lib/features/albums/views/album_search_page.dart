import 'package:albums_frontend/features/albums/bloc/albums_bloc.dart';
import 'package:albums_frontend/features/albums/bloc/albums_event.dart';
import 'package:albums_frontend/features/albums/bloc/albums_state.dart';
import 'package:albums_frontend/features/albums/views/widgets/album_card.dart';
import 'package:albums_frontend/features/albums/views/widgets/album_create_dialog.dart';
import 'package:albums_frontend/features/albums/views/widgets/album_detail_sheet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AlbumSearchPage extends StatelessWidget {
  const AlbumSearchPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Albums')),
      floatingActionButton: FloatingActionButton(
        onPressed: () => showDialog<void>(
          context: context,
          builder: (_) => const AlbumCreateDialog(),
        ),
        child: const Icon(Icons.add),
      ),
      body: BlocConsumer<AlbumsBloc, AlbumsState>(
        listener: (context, state) {
          if (state.selectedAlbum != null) {
            showModalBottomSheet<void>(
              context: context,
              isScrollControlled: true,
              builder: (_) => AlbumDetailSheet(album: state.selectedAlbum!),
            );
          }
          if (state.error != null) {
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.error!)));
          }
        },
        builder: (context, state) {
          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(12),
                child: SearchBar(
                  hintText: 'Search title, artist, producer',
                  onChanged: (value) => context.read<AlbumsBloc>().add(AlbumsSearchChanged(value)),
                ),
              ),
              if (state.loading) const LinearProgressIndicator(),
              Expanded(
                child: ListView.builder(
                  itemCount: state.results.length,
                  itemBuilder: (context, index) {
                    final album = state.results[index];
                    return AlbumCard(
                      album: album,
                      onTap: () => context.read<AlbumsBloc>().add(AlbumSelected(album.id)),
                    );
                  },
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
