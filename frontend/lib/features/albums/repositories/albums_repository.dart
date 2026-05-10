import 'package:albums_frontend/generated_api/lib/api.dart';
import 'package:albums_frontend/generated_api/lib/model/models.dart';

class AlbumsRepository {
  AlbumsRepository(this._api);

  final AlbumsApi _api;

  Future<List<AlbumSummary>> listAlbums() => _api.listAlbumsAlbumsGet();

  Future<List<AlbumSummary>> searchAlbums(String query) => _api.searchAlbumsAlbumsSearchGet(q: query);

  Future<AlbumRead> getAlbum(int id) => _api.getAlbumAlbumsAlbumIdGet(albumId: id);

  Future<AlbumRead> createAlbum(Map<String, dynamic> payload) => _api.createAlbumAlbumsPost(albumCreate: AlbumCreate.fromJson(payload));
}
