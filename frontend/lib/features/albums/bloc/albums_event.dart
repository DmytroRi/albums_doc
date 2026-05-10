import 'package:equatable/equatable.dart';

abstract class AlbumsEvent extends Equatable {
  const AlbumsEvent();

  @override
  List<Object?> get props => [];
}

class AlbumsSearchChanged extends AlbumsEvent {
  const AlbumsSearchChanged(this.query);

  final String query;

  @override
  List<Object?> get props => [query];
}

class AlbumSelected extends AlbumsEvent {
  const AlbumSelected(this.albumId);

  final int albumId;

  @override
  List<Object?> get props => [albumId];
}

class AlbumCreateSubmitted extends AlbumsEvent {
  const AlbumCreateSubmitted(this.payload);

  final Map<String, dynamic> payload;

  @override
  List<Object?> get props => [payload];
}
