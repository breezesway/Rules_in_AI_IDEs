// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_details_viewmodel.var.gql.dart';

// **************************************************************************
// BuiltValueGenerator
// **************************************************************************

Serializer<GGetUserDetailsVars> _$gGetUserDetailsVarsSerializer =
    _$GGetUserDetailsVarsSerializer();
Serializer<GGetUserRepositoriesVars> _$gGetUserRepositoriesVarsSerializer =
    _$GGetUserRepositoriesVarsSerializer();

class _$GGetUserDetailsVarsSerializer
    implements StructuredSerializer<GGetUserDetailsVars> {
  @override
  final Iterable<Type> types = const [
    GGetUserDetailsVars,
    _$GGetUserDetailsVars,
  ];
  @override
  final String wireName = 'GGetUserDetailsVars';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserDetailsVars object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      'login',
      serializers.serialize(
        object.login,
        specifiedType: const FullType(String),
      ),
    ];

    return result;
  }

  @override
  GGetUserDetailsVars deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserDetailsVarsBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case 'login':
          result.login =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserRepositoriesVarsSerializer
    implements StructuredSerializer<GGetUserRepositoriesVars> {
  @override
  final Iterable<Type> types = const [
    GGetUserRepositoriesVars,
    _$GGetUserRepositoriesVars,
  ];
  @override
  final String wireName = 'GGetUserRepositoriesVars';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserRepositoriesVars object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      'login',
      serializers.serialize(
        object.login,
        specifiedType: const FullType(String),
      ),
      'first',
      serializers.serialize(object.first, specifiedType: const FullType(int)),
    ];
    Object? value;
    value = object.after;
    if (value != null) {
      result
        ..add('after')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    return result;
  }

  @override
  GGetUserRepositoriesVars deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserRepositoriesVarsBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case 'login':
          result.login =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'first':
          result.first =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(int),
                  )!
                  as int;
          break;
        case 'after':
          result.after =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )
                  as String?;
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserDetailsVars extends GGetUserDetailsVars {
  @override
  final String login;

  factory _$GGetUserDetailsVars([
    void Function(GGetUserDetailsVarsBuilder)? updates,
  ]) => (GGetUserDetailsVarsBuilder()..update(updates))._build();

  _$GGetUserDetailsVars._({required this.login}) : super._();
  @override
  GGetUserDetailsVars rebuild(
    void Function(GGetUserDetailsVarsBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserDetailsVarsBuilder toBuilder() =>
      GGetUserDetailsVarsBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserDetailsVars && login == other.login;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, login.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(
      r'GGetUserDetailsVars',
    )..add('login', login)).toString();
  }
}

class GGetUserDetailsVarsBuilder
    implements Builder<GGetUserDetailsVars, GGetUserDetailsVarsBuilder> {
  _$GGetUserDetailsVars? _$v;

  String? _login;
  String? get login => _$this._login;
  set login(String? login) => _$this._login = login;

  GGetUserDetailsVarsBuilder();

  GGetUserDetailsVarsBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _login = $v.login;
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserDetailsVars other) {
    _$v = other as _$GGetUserDetailsVars;
  }

  @override
  void update(void Function(GGetUserDetailsVarsBuilder)? updates) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserDetailsVars build() => _build();

  _$GGetUserDetailsVars _build() {
    final _$result =
        _$v ??
        _$GGetUserDetailsVars._(
          login: BuiltValueNullFieldError.checkNotNull(
            login,
            r'GGetUserDetailsVars',
            'login',
          ),
        );
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserRepositoriesVars extends GGetUserRepositoriesVars {
  @override
  final String login;
  @override
  final int first;
  @override
  final String? after;

  factory _$GGetUserRepositoriesVars([
    void Function(GGetUserRepositoriesVarsBuilder)? updates,
  ]) => (GGetUserRepositoriesVarsBuilder()..update(updates))._build();

  _$GGetUserRepositoriesVars._({
    required this.login,
    required this.first,
    this.after,
  }) : super._();
  @override
  GGetUserRepositoriesVars rebuild(
    void Function(GGetUserRepositoriesVarsBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserRepositoriesVarsBuilder toBuilder() =>
      GGetUserRepositoriesVarsBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserRepositoriesVars &&
        login == other.login &&
        first == other.first &&
        after == other.after;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, login.hashCode);
    _$hash = $jc(_$hash, first.hashCode);
    _$hash = $jc(_$hash, after.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(r'GGetUserRepositoriesVars')
          ..add('login', login)
          ..add('first', first)
          ..add('after', after))
        .toString();
  }
}

class GGetUserRepositoriesVarsBuilder
    implements
        Builder<GGetUserRepositoriesVars, GGetUserRepositoriesVarsBuilder> {
  _$GGetUserRepositoriesVars? _$v;

  String? _login;
  String? get login => _$this._login;
  set login(String? login) => _$this._login = login;

  int? _first;
  int? get first => _$this._first;
  set first(int? first) => _$this._first = first;

  String? _after;
  String? get after => _$this._after;
  set after(String? after) => _$this._after = after;

  GGetUserRepositoriesVarsBuilder();

  GGetUserRepositoriesVarsBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _login = $v.login;
      _first = $v.first;
      _after = $v.after;
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserRepositoriesVars other) {
    _$v = other as _$GGetUserRepositoriesVars;
  }

  @override
  void update(void Function(GGetUserRepositoriesVarsBuilder)? updates) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserRepositoriesVars build() => _build();

  _$GGetUserRepositoriesVars _build() {
    final _$result =
        _$v ??
        _$GGetUserRepositoriesVars._(
          login: BuiltValueNullFieldError.checkNotNull(
            login,
            r'GGetUserRepositoriesVars',
            'login',
          ),
          first: BuiltValueNullFieldError.checkNotNull(
            first,
            r'GGetUserRepositoriesVars',
            'first',
          ),
          after: after,
        );
    replace(_$result);
    return _$result;
  }
}

// ignore_for_file: deprecated_member_use_from_same_package,type=lint
