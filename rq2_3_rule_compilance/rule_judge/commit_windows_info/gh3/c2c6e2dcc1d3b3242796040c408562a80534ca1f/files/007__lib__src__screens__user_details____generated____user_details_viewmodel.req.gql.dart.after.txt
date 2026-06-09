// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint

// ignore_for_file: no_leading_underscores_for_library_prefixes
import 'package:built_value/built_value.dart';
import 'package:built_value/serializer.dart';
import 'package:ferry_exec/ferry_exec.dart' as _i1;
import 'package:gh3/__generated__/serializers.gql.dart' as _i6;
import 'package:gh3/src/screens/user_details/__generated__/user_details_viewmodel.ast.gql.dart'
    as _i5;
import 'package:gh3/src/screens/user_details/__generated__/user_details_viewmodel.data.gql.dart'
    as _i2;
import 'package:gh3/src/screens/user_details/__generated__/user_details_viewmodel.var.gql.dart'
    as _i3;
import 'package:gql_exec/gql_exec.dart' as _i4;

part 'user_details_viewmodel.req.gql.g.dart';

abstract class GGetUserDetailsReq
    implements
        Built<GGetUserDetailsReq, GGetUserDetailsReqBuilder>,
        _i1.OperationRequest<_i2.GGetUserDetailsData, _i3.GGetUserDetailsVars> {
  GGetUserDetailsReq._();

  factory GGetUserDetailsReq([
    void Function(GGetUserDetailsReqBuilder b) updates,
  ]) = _$GGetUserDetailsReq;

  static void _initializeBuilder(GGetUserDetailsReqBuilder b) => b
    ..operation = _i4.Operation(
      document: _i5.document,
      operationName: 'GetUserDetails',
    )
    ..executeOnListen = true;

  @override
  _i3.GGetUserDetailsVars get vars;
  @override
  _i4.Operation get operation;
  @override
  _i4.Request get execRequest => _i4.Request(
    operation: operation,
    variables: vars.toJson(),
    context: context ?? const _i4.Context(),
  );

  @override
  String? get requestId;
  @override
  @BuiltValueField(serialize: false)
  _i2.GGetUserDetailsData? Function(
    _i2.GGetUserDetailsData?,
    _i2.GGetUserDetailsData?,
  )?
  get updateResult;
  @override
  _i2.GGetUserDetailsData? get optimisticResponse;
  @override
  String? get updateCacheHandlerKey;
  @override
  Map<String, dynamic>? get updateCacheHandlerContext;
  @override
  _i1.FetchPolicy? get fetchPolicy;
  @override
  bool get executeOnListen;
  @override
  @BuiltValueField(serialize: false)
  _i4.Context? get context;
  @override
  _i2.GGetUserDetailsData? parseData(Map<String, dynamic> json) =>
      _i2.GGetUserDetailsData.fromJson(json);

  @override
  Map<String, dynamic> varsToJson() => vars.toJson();

  @override
  Map<String, dynamic> dataToJson(_i2.GGetUserDetailsData data) =>
      data.toJson();

  @override
  _i1.OperationRequest<_i2.GGetUserDetailsData, _i3.GGetUserDetailsVars>
  transformOperation(_i4.Operation Function(_i4.Operation) transform) =>
      this.rebuild((b) => b..operation = transform(operation));

  static Serializer<GGetUserDetailsReq> get serializer =>
      _$gGetUserDetailsReqSerializer;

  Map<String, dynamic> toJson() =>
      (_i6.serializers.serializeWith(GGetUserDetailsReq.serializer, this)
          as Map<String, dynamic>);

  static GGetUserDetailsReq? fromJson(Map<String, dynamic> json) =>
      _i6.serializers.deserializeWith(GGetUserDetailsReq.serializer, json);
}

abstract class GGetUserRepositoriesReq
    implements
        Built<GGetUserRepositoriesReq, GGetUserRepositoriesReqBuilder>,
        _i1.OperationRequest<
          _i2.GGetUserRepositoriesData,
          _i3.GGetUserRepositoriesVars
        > {
  GGetUserRepositoriesReq._();

  factory GGetUserRepositoriesReq([
    void Function(GGetUserRepositoriesReqBuilder b) updates,
  ]) = _$GGetUserRepositoriesReq;

  static void _initializeBuilder(GGetUserRepositoriesReqBuilder b) => b
    ..operation = _i4.Operation(
      document: _i5.document,
      operationName: 'GetUserRepositories',
    )
    ..executeOnListen = true;

  @override
  _i3.GGetUserRepositoriesVars get vars;
  @override
  _i4.Operation get operation;
  @override
  _i4.Request get execRequest => _i4.Request(
    operation: operation,
    variables: vars.toJson(),
    context: context ?? const _i4.Context(),
  );

  @override
  String? get requestId;
  @override
  @BuiltValueField(serialize: false)
  _i2.GGetUserRepositoriesData? Function(
    _i2.GGetUserRepositoriesData?,
    _i2.GGetUserRepositoriesData?,
  )?
  get updateResult;
  @override
  _i2.GGetUserRepositoriesData? get optimisticResponse;
  @override
  String? get updateCacheHandlerKey;
  @override
  Map<String, dynamic>? get updateCacheHandlerContext;
  @override
  _i1.FetchPolicy? get fetchPolicy;
  @override
  bool get executeOnListen;
  @override
  @BuiltValueField(serialize: false)
  _i4.Context? get context;
  @override
  _i2.GGetUserRepositoriesData? parseData(Map<String, dynamic> json) =>
      _i2.GGetUserRepositoriesData.fromJson(json);

  @override
  Map<String, dynamic> varsToJson() => vars.toJson();

  @override
  Map<String, dynamic> dataToJson(_i2.GGetUserRepositoriesData data) =>
      data.toJson();

  @override
  _i1.OperationRequest<
    _i2.GGetUserRepositoriesData,
    _i3.GGetUserRepositoriesVars
  >
  transformOperation(_i4.Operation Function(_i4.Operation) transform) =>
      this.rebuild((b) => b..operation = transform(operation));

  static Serializer<GGetUserRepositoriesReq> get serializer =>
      _$gGetUserRepositoriesReqSerializer;

  Map<String, dynamic> toJson() =>
      (_i6.serializers.serializeWith(GGetUserRepositoriesReq.serializer, this)
          as Map<String, dynamic>);

  static GGetUserRepositoriesReq? fromJson(Map<String, dynamic> json) =>
      _i6.serializers.deserializeWith(GGetUserRepositoriesReq.serializer, json);
}
