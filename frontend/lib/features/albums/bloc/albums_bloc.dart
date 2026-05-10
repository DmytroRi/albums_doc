import 'package:albums_frontend/features/albums/bloc/albums_event.dart';
import 'package:albums_frontend/features/albums/bloc/albums_state.dart';
import 'package:albums_frontend/features/albums/repositories/albums_repository.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AlbumsBloc extends Bloc<AlbumsEvent, AlbumsState> {
  AlbumsBloc(this._repository) : super(const AlbumsState()) {
    on<AlbumsSearchChanged>(_onSearchChanged);
    on<AlbumSelected>(_onAlbumSelected);
    on<AlbumCreateSubmitted>(_onAlbumCreateSubmitted);
  }

  final AlbumsRepository _repository;

  Future<void> _onSearchChanged(AlbumsSearchChanged event, Emitter<AlbumsState> emit) async {
    emit(state.copyWith(query: event.query, loading: true, clearError: true));
    try {
      final data = event.query.trim().isEmpty
          ? await _repository.listAlbums()
          : await _repository.searchAlbums(event.query);
      emit(state.copyWith(results: data, loading: false));
    } catch (e) {
      emit(state.copyWith(loading: false, error: e.toString()));
    }
  }

  Future<void> _onAlbumSelected(AlbumSelected event, Emitter<AlbumsState> emit) async {
    emit(state.copyWith(loading: true, clearError: true));
    try {
      final album = await _repository.getAlbum(event.albumId);
      emit(state.copyWith(selectedAlbum: album, loading: false));
    } catch (e) {
      emit(state.copyWith(loading: false, error: e.toString()));
    }
  }

  Future<void> _onAlbumCreateSubmitted(AlbumCreateSubmitted event, Emitter<AlbumsState> emit) async {
    emit(state.copyWith(loading: true, clearError: true));
    try {
      await _repository.createAlbum(event.payload);
      final refreshed = state.query.trim().isEmpty
          ? await _repository.listAlbums()
          : await _repository.searchAlbums(state.query);
      emit(state.copyWith(results: refreshed, loading: false));
    } catch (e) {
      emit(state.copyWith(loading: false, error: e.toString()));
    }
  }
}
