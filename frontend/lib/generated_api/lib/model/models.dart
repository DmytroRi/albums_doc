class AlbumSummary {
  AlbumSummary({required this.id, required this.title, required this.releaseYear, required this.grade, required this.artists});
  final int id;
  final String title;
  final int releaseYear;
  final double grade;
  final List<String> artists;
  factory AlbumSummary.fromJson(Map<String, dynamic> json) => AlbumSummary(
        id: json['id'],
        title: json['title'],
        releaseYear: json['release_year'],
        grade: (json['grade'] as num).toDouble(),
        artists: (json['artists'] as List).cast<String>(),
      );
}

class TrackRead {
  TrackRead({required this.id, required this.title, required this.durationSeconds, required this.trackOrder});
  final int id;
  final String title;
  final int durationSeconds;
  final int trackOrder;
  factory TrackRead.fromJson(Map<String, dynamic> json) => TrackRead(
        id: json['id'],
        title: json['title'],
        durationSeconds: json['duration_seconds'],
        trackOrder: json['track_order'],
      );
}

class AlbumRead extends AlbumSummary {
  AlbumRead({
    required super.id,
    required super.title,
    required super.releaseYear,
    required super.grade,
    required super.artists,
    required this.producers,
    required this.genres,
    required this.moods,
    required this.tracks,
  });
  final List<String> producers;
  final List<String> genres;
  final List<String> moods;
  final List<TrackRead> tracks;
  factory AlbumRead.fromJson(Map<String, dynamic> json) => AlbumRead(
        id: json['id'],
        title: json['title'],
        releaseYear: json['release_year'],
        grade: (json['grade'] as num).toDouble(),
        artists: (json['artists'] as List).cast<String>(),
        producers: (json['producers'] as List).cast<String>(),
        genres: (json['genres'] as List).cast<String>(),
        moods: (json['moods'] as List).cast<String>(),
        tracks: (json['tracks'] as List).map((e) => TrackRead.fromJson(e)).toList(),
      );
}

class AlbumCreate {
  AlbumCreate({required this.payload});
  final Map<String, dynamic> payload;
  factory AlbumCreate.fromJson(Map<String, dynamic> json) => AlbumCreate(payload: json);
  Map<String, dynamic> toJson() => payload;
}
