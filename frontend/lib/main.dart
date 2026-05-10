import 'package:albums_frontend/app/albums_app.dart';
import 'package:albums_frontend/features/albums/bloc/albums_bloc.dart';
import 'package:albums_frontend/features/albums/bloc/albums_event.dart';
import 'package:albums_frontend/features/albums/repositories/albums_repository.dart';
import 'package:albums_frontend/generated_api/lib/api.dart';
import 'package:flutter/material.dart';

void main() {
  final apiClient = ApiClient(basePath: const String.fromEnvironment('API_BASE_URL', defaultValue: 'http://localhost:8000'));
  final albumsApi = AlbumsApi(apiClient);
  final repository = AlbumsRepository(albumsApi);

  runApp(
    AlbumsApp(
      albumsBloc: AlbumsBloc(repository)
        ..add(const AlbumsSearchChanged('')),
    ),
  );
}
