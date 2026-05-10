import 'package:dio/dio.dart';

class ApiClient {
  ApiClient({required this.basePath}) : dio = Dio(BaseOptions(baseUrl: basePath));
  final String basePath;
  final Dio dio;
}
