import 'package:albums_frontend/generated_api/lib/model/models.dart';
import 'package:equatable/equatable.dart';

class AlbumsState extends Equatable {
  const AlbumsState({
    this.query = '',
    this.results = const [],
    this.selectedAlbum,
    this.loading = false,
    this.error,
  });

  final String query;
  final List<AlbumSummary> results;
  final AlbumRead? selectedAlbum;
  final bool loading;
  final String? error;

  AlbumsState copyWith({
    String? query,
    List<AlbumSummary>? results,
    AlbumRead? selectedAlbum,
    bool clearSelected = false,
    bool? loading,
    String? error,
    bool clearError = false,
  }) {
    return AlbumsState(
      query: query ?? this.query,
      results: results ?? this.results,
      selectedAlbum: clearSelected ? null : (selectedAlbum ?? this.selectedAlbum),
      loading: loading ?? this.loading,
      error: clearError ? null : (error ?? this.error),
    );
  }

  @override
  List<Object?> get props => [query, results, selectedAlbum, loading, error];
}
