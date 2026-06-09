// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint

// ignore_for_file: no_leading_underscores_for_library_prefixes
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:gh3/__generated__/serializers.gql.dart' as _i1;

part 'user_details_viewmodel.var.gql.g.dart';

abstract class GGetUserDetailsVars
    implements Built<GGetUserDetailsVars, GGetUserDetailsVarsBuilder> {
  GGetUserDetailsVars._();

  factory GGetUserDetailsVars([
    void Function(GGetUserDetailsVarsBuilder b) updates,
  ]) = _$GGetUserDetailsVars;

  String get login;
  static Serializer<GGetUserDetailsVars> get serializer =>
      _$gGetUserDetailsVarsSerializer;

  Map<String, dynamic> toJson() =>
      (_i1.serializers.serializeWith(GGetUserDetailsVars.serializer, this)
          as Map<String, dynamic>);

  static GGetUserDetailsVars? fromJson(Map<String, dynamic> json) =>
      _i1.serializers.deserializeWith(GGetUserDetailsVars.serializer, json);
}

abstract class GGetUserRepositoriesVars
    implements
        Built<GGetUserRepositoriesVars, GGetUserRepositoriesVarsBuilder> {
  GGetUserRepositoriesVars._();

  factory GGetUserRepositoriesVars([
    void Function(GGetUserRepositoriesVarsBuilder b) updates,
  ]) = _$GGetUserRepositoriesVars;

  String get login;
  int get first;
  String? get after;
  static Serializer<GGetUserRepositoriesVars> get serializer =>
      _$gGetUserRepositoriesVarsSerializer;

  Map<String, dynamic> toJson() =>
      (_i1.serializers.serializeWith(GGetUserRepositoriesVars.serializer, this)
          as Map<String, dynamic>);

  static GGetUserRepositoriesVars? fromJson(Map<String, dynamic> json) => _i1
      .serializers
      .deserializeWith(GGetUserRepositoriesVars.serializer, json);
}
