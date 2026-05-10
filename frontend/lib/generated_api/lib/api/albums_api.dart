import 'package:albums_frontend/generated_api/lib/api_client.dart';
import 'package:albums_frontend/generated_api/lib/model/models.dart';

class AlbumsApi {
  AlbumsApi(this.apiClient);
  final ApiClient apiClient;

  Future<AlbumRead> createAlbumAlbumsPost({required AlbumCreate albumCreate}) async {
    final response = await apiClient.dio.post('/albums', data: albumCreate.toJson());
    return AlbumRead.fromJson(response.data);
  }

  Future<AlbumRead> getAlbumAlbumsAlbumIdGet({required int albumId}) async {
    final response = await apiClient.dio.get('/albums/$albumId');
    return AlbumRead.fromJson(response.data);
  }

  Future<List<AlbumSummary>> listAlbumsAlbumsGet() async {
    final response = await apiClient.dio.get('/albums');
    return (response.data as List).map((e) => AlbumSummary.fromJson(e)).toList();
  }

  Future<List<AlbumSummary>> searchAlbumsAlbumsSearchGet({required String q}) async {
    final response = await apiClient.dio.get('/albums/search', queryParameters: {'q': q});
    return (response.data as List).map((e) => AlbumSummary.fromJson(e)).toList();
  }
}
