import 'package:albums_frontend/features/albums/bloc/albums_bloc.dart';
import 'package:albums_frontend/features/albums/views/album_search_page.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AlbumsApp extends StatelessWidget {
  const AlbumsApp({super.key, required this.albumsBloc});

  final AlbumsBloc albumsBloc;

  @override
  Widget build(BuildContext context) {
    return BlocProvider.value(
      value: albumsBloc,
      child: MaterialApp(
        title: 'Albums',
        theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.indigo),
        home: const AlbumSearchPage(),
      ),
    );
  }
}
