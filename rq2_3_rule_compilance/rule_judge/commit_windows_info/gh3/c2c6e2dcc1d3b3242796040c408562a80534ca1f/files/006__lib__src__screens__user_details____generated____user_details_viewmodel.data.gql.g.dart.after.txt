// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_details_viewmodel.data.gql.dart';

// **************************************************************************
// BuiltValueGenerator
// **************************************************************************

Serializer<GGetUserDetailsData> _$gGetUserDetailsDataSerializer =
    _$GGetUserDetailsDataSerializer();
Serializer<GGetUserDetailsData_user> _$gGetUserDetailsDataUserSerializer =
    _$GGetUserDetailsData_userSerializer();
Serializer<GGetUserDetailsData_user_repositories>
_$gGetUserDetailsDataUserRepositoriesSerializer =
    _$GGetUserDetailsData_user_repositoriesSerializer();
Serializer<GGetUserDetailsData_user_followers>
_$gGetUserDetailsDataUserFollowersSerializer =
    _$GGetUserDetailsData_user_followersSerializer();
Serializer<GGetUserDetailsData_user_following>
_$gGetUserDetailsDataUserFollowingSerializer =
    _$GGetUserDetailsData_user_followingSerializer();
Serializer<GGetUserRepositoriesData> _$gGetUserRepositoriesDataSerializer =
    _$GGetUserRepositoriesDataSerializer();
Serializer<GGetUserRepositoriesData_user>
_$gGetUserRepositoriesDataUserSerializer =
    _$GGetUserRepositoriesData_userSerializer();
Serializer<GGetUserRepositoriesData_user_repositories>
_$gGetUserRepositoriesDataUserRepositoriesSerializer =
    _$GGetUserRepositoriesData_user_repositoriesSerializer();
Serializer<GGetUserRepositoriesData_user_repositories_nodes>
_$gGetUserRepositoriesDataUserRepositoriesNodesSerializer =
    _$GGetUserRepositoriesData_user_repositories_nodesSerializer();
Serializer<GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage>
_$gGetUserRepositoriesDataUserRepositoriesNodesPrimaryLanguageSerializer =
    _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageSerializer();
Serializer<GGetUserRepositoriesData_user_repositories_pageInfo>
_$gGetUserRepositoriesDataUserRepositoriesPageInfoSerializer =
    _$GGetUserRepositoriesData_user_repositories_pageInfoSerializer();

class _$GGetUserDetailsDataSerializer
    implements StructuredSerializer<GGetUserDetailsData> {
  @override
  final Iterable<Type> types = const [
    GGetUserDetailsData,
    _$GGetUserDetailsData,
  ];
  @override
  final String wireName = 'GGetUserDetailsData';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserDetailsData object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
    ];
    Object? value;
    value = object.user;
    if (value != null) {
      result
        ..add('user')
        ..add(
          serializers.serialize(
            value,
            specifiedType: const FullType(GGetUserDetailsData_user),
          ),
        );
    }
    return result;
  }

  @override
  GGetUserDetailsData deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserDetailsDataBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'user':
          result.user.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(GGetUserDetailsData_user),
                )!
                as GGetUserDetailsData_user,
          );
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserDetailsData_userSerializer
    implements StructuredSerializer<GGetUserDetailsData_user> {
  @override
  final Iterable<Type> types = const [
    GGetUserDetailsData_user,
    _$GGetUserDetailsData_user,
  ];
  @override
  final String wireName = 'GGetUserDetailsData_user';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserDetailsData_user object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'id',
      serializers.serialize(object.id, specifiedType: const FullType(String)),
      'login',
      serializers.serialize(
        object.login,
        specifiedType: const FullType(String),
      ),
      'email',
      serializers.serialize(
        object.email,
        specifiedType: const FullType(String),
      ),
      'avatarUrl',
      serializers.serialize(
        object.avatarUrl,
        specifiedType: const FullType(_i3.GURI),
      ),
      'url',
      serializers.serialize(
        object.url,
        specifiedType: const FullType(_i3.GURI),
      ),
      'repositories',
      serializers.serialize(
        object.repositories,
        specifiedType: const FullType(GGetUserDetailsData_user_repositories),
      ),
      'followers',
      serializers.serialize(
        object.followers,
        specifiedType: const FullType(GGetUserDetailsData_user_followers),
      ),
      'following',
      serializers.serialize(
        object.following,
        specifiedType: const FullType(GGetUserDetailsData_user_following),
      ),
      'createdAt',
      serializers.serialize(
        object.createdAt,
        specifiedType: const FullType(_i3.GDateTime),
      ),
      'updatedAt',
      serializers.serialize(
        object.updatedAt,
        specifiedType: const FullType(_i3.GDateTime),
      ),
    ];
    Object? value;
    value = object.name;
    if (value != null) {
      result
        ..add('name')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    value = object.bio;
    if (value != null) {
      result
        ..add('bio')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    value = object.location;
    if (value != null) {
      result
        ..add('location')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    value = object.company;
    if (value != null) {
      result
        ..add('company')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    value = object.websiteUrl;
    if (value != null) {
      result
        ..add('websiteUrl')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(_i3.GURI)),
        );
    }
    return result;
  }

  @override
  GGetUserDetailsData_user deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserDetailsData_userBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'id':
          result.id =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'login':
          result.login =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'name':
          result.name =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )
                  as String?;
          break;
        case 'email':
          result.email =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'bio':
          result.bio =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )
                  as String?;
          break;
        case 'location':
          result.location =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )
                  as String?;
          break;
        case 'company':
          result.company =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )
                  as String?;
          break;
        case 'websiteUrl':
          result.websiteUrl.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(_i3.GURI),
                )!
                as _i3.GURI,
          );
          break;
        case 'avatarUrl':
          result.avatarUrl.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(_i3.GURI),
                )!
                as _i3.GURI,
          );
          break;
        case 'url':
          result.url.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(_i3.GURI),
                )!
                as _i3.GURI,
          );
          break;
        case 'repositories':
          result.repositories.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(
                    GGetUserDetailsData_user_repositories,
                  ),
                )!
                as GGetUserDetailsData_user_repositories,
          );
          break;
        case 'followers':
          result.followers.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(
                    GGetUserDetailsData_user_followers,
                  ),
                )!
                as GGetUserDetailsData_user_followers,
          );
          break;
        case 'following':
          result.following.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(
                    GGetUserDetailsData_user_following,
                  ),
                )!
                as GGetUserDetailsData_user_following,
          );
          break;
        case 'createdAt':
          result.createdAt.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(_i3.GDateTime),
                )!
                as _i3.GDateTime,
          );
          break;
        case 'updatedAt':
          result.updatedAt.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(_i3.GDateTime),
                )!
                as _i3.GDateTime,
          );
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserDetailsData_user_repositoriesSerializer
    implements StructuredSerializer<GGetUserDetailsData_user_repositories> {
  @override
  final Iterable<Type> types = const [
    GGetUserDetailsData_user_repositories,
    _$GGetUserDetailsData_user_repositories,
  ];
  @override
  final String wireName = 'GGetUserDetailsData_user_repositories';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserDetailsData_user_repositories object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'totalCount',
      serializers.serialize(
        object.totalCount,
        specifiedType: const FullType(int),
      ),
    ];

    return result;
  }

  @override
  GGetUserDetailsData_user_repositories deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserDetailsData_user_repositoriesBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'totalCount':
          result.totalCount =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(int),
                  )!
                  as int;
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserDetailsData_user_followersSerializer
    implements StructuredSerializer<GGetUserDetailsData_user_followers> {
  @override
  final Iterable<Type> types = const [
    GGetUserDetailsData_user_followers,
    _$GGetUserDetailsData_user_followers,
  ];
  @override
  final String wireName = 'GGetUserDetailsData_user_followers';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserDetailsData_user_followers object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'totalCount',
      serializers.serialize(
        object.totalCount,
        specifiedType: const FullType(int),
      ),
    ];

    return result;
  }

  @override
  GGetUserDetailsData_user_followers deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserDetailsData_user_followersBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'totalCount':
          result.totalCount =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(int),
                  )!
                  as int;
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserDetailsData_user_followingSerializer
    implements StructuredSerializer<GGetUserDetailsData_user_following> {
  @override
  final Iterable<Type> types = const [
    GGetUserDetailsData_user_following,
    _$GGetUserDetailsData_user_following,
  ];
  @override
  final String wireName = 'GGetUserDetailsData_user_following';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserDetailsData_user_following object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'totalCount',
      serializers.serialize(
        object.totalCount,
        specifiedType: const FullType(int),
      ),
    ];

    return result;
  }

  @override
  GGetUserDetailsData_user_following deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserDetailsData_user_followingBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'totalCount':
          result.totalCount =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(int),
                  )!
                  as int;
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserRepositoriesDataSerializer
    implements StructuredSerializer<GGetUserRepositoriesData> {
  @override
  final Iterable<Type> types = const [
    GGetUserRepositoriesData,
    _$GGetUserRepositoriesData,
  ];
  @override
  final String wireName = 'GGetUserRepositoriesData';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserRepositoriesData object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
    ];
    Object? value;
    value = object.user;
    if (value != null) {
      result
        ..add('user')
        ..add(
          serializers.serialize(
            value,
            specifiedType: const FullType(GGetUserRepositoriesData_user),
          ),
        );
    }
    return result;
  }

  @override
  GGetUserRepositoriesData deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserRepositoriesDataBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'user':
          result.user.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(GGetUserRepositoriesData_user),
                )!
                as GGetUserRepositoriesData_user,
          );
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserRepositoriesData_userSerializer
    implements StructuredSerializer<GGetUserRepositoriesData_user> {
  @override
  final Iterable<Type> types = const [
    GGetUserRepositoriesData_user,
    _$GGetUserRepositoriesData_user,
  ];
  @override
  final String wireName = 'GGetUserRepositoriesData_user';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserRepositoriesData_user object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'repositories',
      serializers.serialize(
        object.repositories,
        specifiedType: const FullType(
          GGetUserRepositoriesData_user_repositories,
        ),
      ),
    ];

    return result;
  }

  @override
  GGetUserRepositoriesData_user deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserRepositoriesData_userBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'repositories':
          result.repositories.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(
                    GGetUserRepositoriesData_user_repositories,
                  ),
                )!
                as GGetUserRepositoriesData_user_repositories,
          );
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserRepositoriesData_user_repositoriesSerializer
    implements
        StructuredSerializer<GGetUserRepositoriesData_user_repositories> {
  @override
  final Iterable<Type> types = const [
    GGetUserRepositoriesData_user_repositories,
    _$GGetUserRepositoriesData_user_repositories,
  ];
  @override
  final String wireName = 'GGetUserRepositoriesData_user_repositories';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserRepositoriesData_user_repositories object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'pageInfo',
      serializers.serialize(
        object.pageInfo,
        specifiedType: const FullType(
          GGetUserRepositoriesData_user_repositories_pageInfo,
        ),
      ),
    ];
    Object? value;
    value = object.nodes;
    if (value != null) {
      result
        ..add('nodes')
        ..add(
          serializers.serialize(
            value,
            specifiedType: const FullType(BuiltList, const [
              const FullType.nullable(
                GGetUserRepositoriesData_user_repositories_nodes,
              ),
            ]),
          ),
        );
    }
    return result;
  }

  @override
  GGetUserRepositoriesData_user_repositories deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserRepositoriesData_user_repositoriesBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'nodes':
          result.nodes.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(BuiltList, const [
                    const FullType.nullable(
                      GGetUserRepositoriesData_user_repositories_nodes,
                    ),
                  ]),
                )!
                as BuiltList<Object?>,
          );
          break;
        case 'pageInfo':
          result.pageInfo.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(
                    GGetUserRepositoriesData_user_repositories_pageInfo,
                  ),
                )!
                as GGetUserRepositoriesData_user_repositories_pageInfo,
          );
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserRepositoriesData_user_repositories_nodesSerializer
    implements
        StructuredSerializer<GGetUserRepositoriesData_user_repositories_nodes> {
  @override
  final Iterable<Type> types = const [
    GGetUserRepositoriesData_user_repositories_nodes,
    _$GGetUserRepositoriesData_user_repositories_nodes,
  ];
  @override
  final String wireName = 'GGetUserRepositoriesData_user_repositories_nodes';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserRepositoriesData_user_repositories_nodes object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'id',
      serializers.serialize(object.id, specifiedType: const FullType(String)),
      'name',
      serializers.serialize(object.name, specifiedType: const FullType(String)),
      'nameWithOwner',
      serializers.serialize(
        object.nameWithOwner,
        specifiedType: const FullType(String),
      ),
      'stargazerCount',
      serializers.serialize(
        object.stargazerCount,
        specifiedType: const FullType(int),
      ),
      'forkCount',
      serializers.serialize(
        object.forkCount,
        specifiedType: const FullType(int),
      ),
      'updatedAt',
      serializers.serialize(
        object.updatedAt,
        specifiedType: const FullType(_i3.GDateTime),
      ),
    ];
    Object? value;
    value = object.description;
    if (value != null) {
      result
        ..add('description')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    value = object.primaryLanguage;
    if (value != null) {
      result
        ..add('primaryLanguage')
        ..add(
          serializers.serialize(
            value,
            specifiedType: const FullType(
              GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage,
            ),
          ),
        );
    }
    return result;
  }

  @override
  GGetUserRepositoriesData_user_repositories_nodes deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserRepositoriesData_user_repositories_nodesBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'id':
          result.id =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'name':
          result.name =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'nameWithOwner':
          result.nameWithOwner =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'description':
          result.description =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )
                  as String?;
          break;
        case 'stargazerCount':
          result.stargazerCount =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(int),
                  )!
                  as int;
          break;
        case 'forkCount':
          result.forkCount =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(int),
                  )!
                  as int;
          break;
        case 'primaryLanguage':
          result.primaryLanguage.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(
                    GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage,
                  ),
                )!
                as GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage,
          );
          break;
        case 'updatedAt':
          result.updatedAt.replace(
            serializers.deserialize(
                  value,
                  specifiedType: const FullType(_i3.GDateTime),
                )!
                as _i3.GDateTime,
          );
          break;
      }
    }

    return result.build();
  }
}

class _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageSerializer
    implements
        StructuredSerializer<
          GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage
        > {
  @override
  final Iterable<Type> types = const [
    GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage,
    _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage,
  ];
  @override
  final String wireName =
      'GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'name',
      serializers.serialize(object.name, specifiedType: const FullType(String)),
    ];
    Object? value;
    value = object.color;
    if (value != null) {
      result
        ..add('color')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    return result;
  }

  @override
  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result =
        GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'name':
          result.name =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'color':
          result.color =
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

class _$GGetUserRepositoriesData_user_repositories_pageInfoSerializer
    implements
        StructuredSerializer<
          GGetUserRepositoriesData_user_repositories_pageInfo
        > {
  @override
  final Iterable<Type> types = const [
    GGetUserRepositoriesData_user_repositories_pageInfo,
    _$GGetUserRepositoriesData_user_repositories_pageInfo,
  ];
  @override
  final String wireName = 'GGetUserRepositoriesData_user_repositories_pageInfo';

  @override
  Iterable<Object?> serialize(
    Serializers serializers,
    GGetUserRepositoriesData_user_repositories_pageInfo object, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = <Object?>[
      '__typename',
      serializers.serialize(
        object.G__typename,
        specifiedType: const FullType(String),
      ),
      'hasNextPage',
      serializers.serialize(
        object.hasNextPage,
        specifiedType: const FullType(bool),
      ),
    ];
    Object? value;
    value = object.endCursor;
    if (value != null) {
      result
        ..add('endCursor')
        ..add(
          serializers.serialize(value, specifiedType: const FullType(String)),
        );
    }
    return result;
  }

  @override
  GGetUserRepositoriesData_user_repositories_pageInfo deserialize(
    Serializers serializers,
    Iterable<Object?> serialized, {
    FullType specifiedType = FullType.unspecified,
  }) {
    final result = GGetUserRepositoriesData_user_repositories_pageInfoBuilder();

    final iterator = serialized.iterator;
    while (iterator.moveNext()) {
      final key = iterator.current! as String;
      iterator.moveNext();
      final Object? value = iterator.current;
      switch (key) {
        case '__typename':
          result.G__typename =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(String),
                  )!
                  as String;
          break;
        case 'hasNextPage':
          result.hasNextPage =
              serializers.deserialize(
                    value,
                    specifiedType: const FullType(bool),
                  )!
                  as bool;
          break;
        case 'endCursor':
          result.endCursor =
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

class _$GGetUserDetailsData extends GGetUserDetailsData {
  @override
  final String G__typename;
  @override
  final GGetUserDetailsData_user? user;

  factory _$GGetUserDetailsData([
    void Function(GGetUserDetailsDataBuilder)? updates,
  ]) => (GGetUserDetailsDataBuilder()..update(updates))._build();

  _$GGetUserDetailsData._({required this.G__typename, this.user}) : super._();
  @override
  GGetUserDetailsData rebuild(
    void Function(GGetUserDetailsDataBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserDetailsDataBuilder toBuilder() =>
      GGetUserDetailsDataBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserDetailsData &&
        G__typename == other.G__typename &&
        user == other.user;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, user.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(r'GGetUserDetailsData')
          ..add('G__typename', G__typename)
          ..add('user', user))
        .toString();
  }
}

class GGetUserDetailsDataBuilder
    implements Builder<GGetUserDetailsData, GGetUserDetailsDataBuilder> {
  _$GGetUserDetailsData? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  GGetUserDetailsData_userBuilder? _user;
  GGetUserDetailsData_userBuilder get user =>
      _$this._user ??= GGetUserDetailsData_userBuilder();
  set user(GGetUserDetailsData_userBuilder? user) => _$this._user = user;

  GGetUserDetailsDataBuilder() {
    GGetUserDetailsData._initializeBuilder(this);
  }

  GGetUserDetailsDataBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _user = $v.user?.toBuilder();
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserDetailsData other) {
    _$v = other as _$GGetUserDetailsData;
  }

  @override
  void update(void Function(GGetUserDetailsDataBuilder)? updates) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserDetailsData build() => _build();

  _$GGetUserDetailsData _build() {
    _$GGetUserDetailsData _$result;
    try {
      _$result =
          _$v ??
          _$GGetUserDetailsData._(
            G__typename: BuiltValueNullFieldError.checkNotNull(
              G__typename,
              r'GGetUserDetailsData',
              'G__typename',
            ),
            user: _user?.build(),
          );
    } catch (_) {
      late String _$failedField;
      try {
        _$failedField = 'user';
        _user?.build();
      } catch (e) {
        throw BuiltValueNestedFieldError(
          r'GGetUserDetailsData',
          _$failedField,
          e.toString(),
        );
      }
      rethrow;
    }
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserDetailsData_user extends GGetUserDetailsData_user {
  @override
  final String G__typename;
  @override
  final String id;
  @override
  final String login;
  @override
  final String? name;
  @override
  final String email;
  @override
  final String? bio;
  @override
  final String? location;
  @override
  final String? company;
  @override
  final _i3.GURI? websiteUrl;
  @override
  final _i3.GURI avatarUrl;
  @override
  final _i3.GURI url;
  @override
  final GGetUserDetailsData_user_repositories repositories;
  @override
  final GGetUserDetailsData_user_followers followers;
  @override
  final GGetUserDetailsData_user_following following;
  @override
  final _i3.GDateTime createdAt;
  @override
  final _i3.GDateTime updatedAt;

  factory _$GGetUserDetailsData_user([
    void Function(GGetUserDetailsData_userBuilder)? updates,
  ]) => (GGetUserDetailsData_userBuilder()..update(updates))._build();

  _$GGetUserDetailsData_user._({
    required this.G__typename,
    required this.id,
    required this.login,
    this.name,
    required this.email,
    this.bio,
    this.location,
    this.company,
    this.websiteUrl,
    required this.avatarUrl,
    required this.url,
    required this.repositories,
    required this.followers,
    required this.following,
    required this.createdAt,
    required this.updatedAt,
  }) : super._();
  @override
  GGetUserDetailsData_user rebuild(
    void Function(GGetUserDetailsData_userBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserDetailsData_userBuilder toBuilder() =>
      GGetUserDetailsData_userBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserDetailsData_user &&
        G__typename == other.G__typename &&
        id == other.id &&
        login == other.login &&
        name == other.name &&
        email == other.email &&
        bio == other.bio &&
        location == other.location &&
        company == other.company &&
        websiteUrl == other.websiteUrl &&
        avatarUrl == other.avatarUrl &&
        url == other.url &&
        repositories == other.repositories &&
        followers == other.followers &&
        following == other.following &&
        createdAt == other.createdAt &&
        updatedAt == other.updatedAt;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, id.hashCode);
    _$hash = $jc(_$hash, login.hashCode);
    _$hash = $jc(_$hash, name.hashCode);
    _$hash = $jc(_$hash, email.hashCode);
    _$hash = $jc(_$hash, bio.hashCode);
    _$hash = $jc(_$hash, location.hashCode);
    _$hash = $jc(_$hash, company.hashCode);
    _$hash = $jc(_$hash, websiteUrl.hashCode);
    _$hash = $jc(_$hash, avatarUrl.hashCode);
    _$hash = $jc(_$hash, url.hashCode);
    _$hash = $jc(_$hash, repositories.hashCode);
    _$hash = $jc(_$hash, followers.hashCode);
    _$hash = $jc(_$hash, following.hashCode);
    _$hash = $jc(_$hash, createdAt.hashCode);
    _$hash = $jc(_$hash, updatedAt.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(r'GGetUserDetailsData_user')
          ..add('G__typename', G__typename)
          ..add('id', id)
          ..add('login', login)
          ..add('name', name)
          ..add('email', email)
          ..add('bio', bio)
          ..add('location', location)
          ..add('company', company)
          ..add('websiteUrl', websiteUrl)
          ..add('avatarUrl', avatarUrl)
          ..add('url', url)
          ..add('repositories', repositories)
          ..add('followers', followers)
          ..add('following', following)
          ..add('createdAt', createdAt)
          ..add('updatedAt', updatedAt))
        .toString();
  }
}

class GGetUserDetailsData_userBuilder
    implements
        Builder<GGetUserDetailsData_user, GGetUserDetailsData_userBuilder> {
  _$GGetUserDetailsData_user? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  String? _id;
  String? get id => _$this._id;
  set id(String? id) => _$this._id = id;

  String? _login;
  String? get login => _$this._login;
  set login(String? login) => _$this._login = login;

  String? _name;
  String? get name => _$this._name;
  set name(String? name) => _$this._name = name;

  String? _email;
  String? get email => _$this._email;
  set email(String? email) => _$this._email = email;

  String? _bio;
  String? get bio => _$this._bio;
  set bio(String? bio) => _$this._bio = bio;

  String? _location;
  String? get location => _$this._location;
  set location(String? location) => _$this._location = location;

  String? _company;
  String? get company => _$this._company;
  set company(String? company) => _$this._company = company;

  _i3.GURIBuilder? _websiteUrl;
  _i3.GURIBuilder get websiteUrl => _$this._websiteUrl ??= _i3.GURIBuilder();
  set websiteUrl(_i3.GURIBuilder? websiteUrl) =>
      _$this._websiteUrl = websiteUrl;

  _i3.GURIBuilder? _avatarUrl;
  _i3.GURIBuilder get avatarUrl => _$this._avatarUrl ??= _i3.GURIBuilder();
  set avatarUrl(_i3.GURIBuilder? avatarUrl) => _$this._avatarUrl = avatarUrl;

  _i3.GURIBuilder? _url;
  _i3.GURIBuilder get url => _$this._url ??= _i3.GURIBuilder();
  set url(_i3.GURIBuilder? url) => _$this._url = url;

  GGetUserDetailsData_user_repositoriesBuilder? _repositories;
  GGetUserDetailsData_user_repositoriesBuilder get repositories =>
      _$this._repositories ??= GGetUserDetailsData_user_repositoriesBuilder();
  set repositories(
    GGetUserDetailsData_user_repositoriesBuilder? repositories,
  ) => _$this._repositories = repositories;

  GGetUserDetailsData_user_followersBuilder? _followers;
  GGetUserDetailsData_user_followersBuilder get followers =>
      _$this._followers ??= GGetUserDetailsData_user_followersBuilder();
  set followers(GGetUserDetailsData_user_followersBuilder? followers) =>
      _$this._followers = followers;

  GGetUserDetailsData_user_followingBuilder? _following;
  GGetUserDetailsData_user_followingBuilder get following =>
      _$this._following ??= GGetUserDetailsData_user_followingBuilder();
  set following(GGetUserDetailsData_user_followingBuilder? following) =>
      _$this._following = following;

  _i3.GDateTimeBuilder? _createdAt;
  _i3.GDateTimeBuilder get createdAt =>
      _$this._createdAt ??= _i3.GDateTimeBuilder();
  set createdAt(_i3.GDateTimeBuilder? createdAt) =>
      _$this._createdAt = createdAt;

  _i3.GDateTimeBuilder? _updatedAt;
  _i3.GDateTimeBuilder get updatedAt =>
      _$this._updatedAt ??= _i3.GDateTimeBuilder();
  set updatedAt(_i3.GDateTimeBuilder? updatedAt) =>
      _$this._updatedAt = updatedAt;

  GGetUserDetailsData_userBuilder() {
    GGetUserDetailsData_user._initializeBuilder(this);
  }

  GGetUserDetailsData_userBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _id = $v.id;
      _login = $v.login;
      _name = $v.name;
      _email = $v.email;
      _bio = $v.bio;
      _location = $v.location;
      _company = $v.company;
      _websiteUrl = $v.websiteUrl?.toBuilder();
      _avatarUrl = $v.avatarUrl.toBuilder();
      _url = $v.url.toBuilder();
      _repositories = $v.repositories.toBuilder();
      _followers = $v.followers.toBuilder();
      _following = $v.following.toBuilder();
      _createdAt = $v.createdAt.toBuilder();
      _updatedAt = $v.updatedAt.toBuilder();
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserDetailsData_user other) {
    _$v = other as _$GGetUserDetailsData_user;
  }

  @override
  void update(void Function(GGetUserDetailsData_userBuilder)? updates) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserDetailsData_user build() => _build();

  _$GGetUserDetailsData_user _build() {
    _$GGetUserDetailsData_user _$result;
    try {
      _$result =
          _$v ??
          _$GGetUserDetailsData_user._(
            G__typename: BuiltValueNullFieldError.checkNotNull(
              G__typename,
              r'GGetUserDetailsData_user',
              'G__typename',
            ),
            id: BuiltValueNullFieldError.checkNotNull(
              id,
              r'GGetUserDetailsData_user',
              'id',
            ),
            login: BuiltValueNullFieldError.checkNotNull(
              login,
              r'GGetUserDetailsData_user',
              'login',
            ),
            name: name,
            email: BuiltValueNullFieldError.checkNotNull(
              email,
              r'GGetUserDetailsData_user',
              'email',
            ),
            bio: bio,
            location: location,
            company: company,
            websiteUrl: _websiteUrl?.build(),
            avatarUrl: avatarUrl.build(),
            url: url.build(),
            repositories: repositories.build(),
            followers: followers.build(),
            following: following.build(),
            createdAt: createdAt.build(),
            updatedAt: updatedAt.build(),
          );
    } catch (_) {
      late String _$failedField;
      try {
        _$failedField = 'websiteUrl';
        _websiteUrl?.build();
        _$failedField = 'avatarUrl';
        avatarUrl.build();
        _$failedField = 'url';
        url.build();
        _$failedField = 'repositories';
        repositories.build();
        _$failedField = 'followers';
        followers.build();
        _$failedField = 'following';
        following.build();
        _$failedField = 'createdAt';
        createdAt.build();
        _$failedField = 'updatedAt';
        updatedAt.build();
      } catch (e) {
        throw BuiltValueNestedFieldError(
          r'GGetUserDetailsData_user',
          _$failedField,
          e.toString(),
        );
      }
      rethrow;
    }
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserDetailsData_user_repositories
    extends GGetUserDetailsData_user_repositories {
  @override
  final String G__typename;
  @override
  final int totalCount;

  factory _$GGetUserDetailsData_user_repositories([
    void Function(GGetUserDetailsData_user_repositoriesBuilder)? updates,
  ]) => (GGetUserDetailsData_user_repositoriesBuilder()..update(updates))
      ._build();

  _$GGetUserDetailsData_user_repositories._({
    required this.G__typename,
    required this.totalCount,
  }) : super._();
  @override
  GGetUserDetailsData_user_repositories rebuild(
    void Function(GGetUserDetailsData_user_repositoriesBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserDetailsData_user_repositoriesBuilder toBuilder() =>
      GGetUserDetailsData_user_repositoriesBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserDetailsData_user_repositories &&
        G__typename == other.G__typename &&
        totalCount == other.totalCount;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, totalCount.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(
            r'GGetUserDetailsData_user_repositories',
          )
          ..add('G__typename', G__typename)
          ..add('totalCount', totalCount))
        .toString();
  }
}

class GGetUserDetailsData_user_repositoriesBuilder
    implements
        Builder<
          GGetUserDetailsData_user_repositories,
          GGetUserDetailsData_user_repositoriesBuilder
        > {
  _$GGetUserDetailsData_user_repositories? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  int? _totalCount;
  int? get totalCount => _$this._totalCount;
  set totalCount(int? totalCount) => _$this._totalCount = totalCount;

  GGetUserDetailsData_user_repositoriesBuilder() {
    GGetUserDetailsData_user_repositories._initializeBuilder(this);
  }

  GGetUserDetailsData_user_repositoriesBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _totalCount = $v.totalCount;
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserDetailsData_user_repositories other) {
    _$v = other as _$GGetUserDetailsData_user_repositories;
  }

  @override
  void update(
    void Function(GGetUserDetailsData_user_repositoriesBuilder)? updates,
  ) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserDetailsData_user_repositories build() => _build();

  _$GGetUserDetailsData_user_repositories _build() {
    final _$result =
        _$v ??
        _$GGetUserDetailsData_user_repositories._(
          G__typename: BuiltValueNullFieldError.checkNotNull(
            G__typename,
            r'GGetUserDetailsData_user_repositories',
            'G__typename',
          ),
          totalCount: BuiltValueNullFieldError.checkNotNull(
            totalCount,
            r'GGetUserDetailsData_user_repositories',
            'totalCount',
          ),
        );
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserDetailsData_user_followers
    extends GGetUserDetailsData_user_followers {
  @override
  final String G__typename;
  @override
  final int totalCount;

  factory _$GGetUserDetailsData_user_followers([
    void Function(GGetUserDetailsData_user_followersBuilder)? updates,
  ]) => (GGetUserDetailsData_user_followersBuilder()..update(updates))._build();

  _$GGetUserDetailsData_user_followers._({
    required this.G__typename,
    required this.totalCount,
  }) : super._();
  @override
  GGetUserDetailsData_user_followers rebuild(
    void Function(GGetUserDetailsData_user_followersBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserDetailsData_user_followersBuilder toBuilder() =>
      GGetUserDetailsData_user_followersBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserDetailsData_user_followers &&
        G__typename == other.G__typename &&
        totalCount == other.totalCount;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, totalCount.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(r'GGetUserDetailsData_user_followers')
          ..add('G__typename', G__typename)
          ..add('totalCount', totalCount))
        .toString();
  }
}

class GGetUserDetailsData_user_followersBuilder
    implements
        Builder<
          GGetUserDetailsData_user_followers,
          GGetUserDetailsData_user_followersBuilder
        > {
  _$GGetUserDetailsData_user_followers? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  int? _totalCount;
  int? get totalCount => _$this._totalCount;
  set totalCount(int? totalCount) => _$this._totalCount = totalCount;

  GGetUserDetailsData_user_followersBuilder() {
    GGetUserDetailsData_user_followers._initializeBuilder(this);
  }

  GGetUserDetailsData_user_followersBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _totalCount = $v.totalCount;
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserDetailsData_user_followers other) {
    _$v = other as _$GGetUserDetailsData_user_followers;
  }

  @override
  void update(
    void Function(GGetUserDetailsData_user_followersBuilder)? updates,
  ) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserDetailsData_user_followers build() => _build();

  _$GGetUserDetailsData_user_followers _build() {
    final _$result =
        _$v ??
        _$GGetUserDetailsData_user_followers._(
          G__typename: BuiltValueNullFieldError.checkNotNull(
            G__typename,
            r'GGetUserDetailsData_user_followers',
            'G__typename',
          ),
          totalCount: BuiltValueNullFieldError.checkNotNull(
            totalCount,
            r'GGetUserDetailsData_user_followers',
            'totalCount',
          ),
        );
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserDetailsData_user_following
    extends GGetUserDetailsData_user_following {
  @override
  final String G__typename;
  @override
  final int totalCount;

  factory _$GGetUserDetailsData_user_following([
    void Function(GGetUserDetailsData_user_followingBuilder)? updates,
  ]) => (GGetUserDetailsData_user_followingBuilder()..update(updates))._build();

  _$GGetUserDetailsData_user_following._({
    required this.G__typename,
    required this.totalCount,
  }) : super._();
  @override
  GGetUserDetailsData_user_following rebuild(
    void Function(GGetUserDetailsData_user_followingBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserDetailsData_user_followingBuilder toBuilder() =>
      GGetUserDetailsData_user_followingBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserDetailsData_user_following &&
        G__typename == other.G__typename &&
        totalCount == other.totalCount;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, totalCount.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(r'GGetUserDetailsData_user_following')
          ..add('G__typename', G__typename)
          ..add('totalCount', totalCount))
        .toString();
  }
}

class GGetUserDetailsData_user_followingBuilder
    implements
        Builder<
          GGetUserDetailsData_user_following,
          GGetUserDetailsData_user_followingBuilder
        > {
  _$GGetUserDetailsData_user_following? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  int? _totalCount;
  int? get totalCount => _$this._totalCount;
  set totalCount(int? totalCount) => _$this._totalCount = totalCount;

  GGetUserDetailsData_user_followingBuilder() {
    GGetUserDetailsData_user_following._initializeBuilder(this);
  }

  GGetUserDetailsData_user_followingBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _totalCount = $v.totalCount;
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserDetailsData_user_following other) {
    _$v = other as _$GGetUserDetailsData_user_following;
  }

  @override
  void update(
    void Function(GGetUserDetailsData_user_followingBuilder)? updates,
  ) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserDetailsData_user_following build() => _build();

  _$GGetUserDetailsData_user_following _build() {
    final _$result =
        _$v ??
        _$GGetUserDetailsData_user_following._(
          G__typename: BuiltValueNullFieldError.checkNotNull(
            G__typename,
            r'GGetUserDetailsData_user_following',
            'G__typename',
          ),
          totalCount: BuiltValueNullFieldError.checkNotNull(
            totalCount,
            r'GGetUserDetailsData_user_following',
            'totalCount',
          ),
        );
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserRepositoriesData extends GGetUserRepositoriesData {
  @override
  final String G__typename;
  @override
  final GGetUserRepositoriesData_user? user;

  factory _$GGetUserRepositoriesData([
    void Function(GGetUserRepositoriesDataBuilder)? updates,
  ]) => (GGetUserRepositoriesDataBuilder()..update(updates))._build();

  _$GGetUserRepositoriesData._({required this.G__typename, this.user})
    : super._();
  @override
  GGetUserRepositoriesData rebuild(
    void Function(GGetUserRepositoriesDataBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserRepositoriesDataBuilder toBuilder() =>
      GGetUserRepositoriesDataBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserRepositoriesData &&
        G__typename == other.G__typename &&
        user == other.user;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, user.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(r'GGetUserRepositoriesData')
          ..add('G__typename', G__typename)
          ..add('user', user))
        .toString();
  }
}

class GGetUserRepositoriesDataBuilder
    implements
        Builder<GGetUserRepositoriesData, GGetUserRepositoriesDataBuilder> {
  _$GGetUserRepositoriesData? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  GGetUserRepositoriesData_userBuilder? _user;
  GGetUserRepositoriesData_userBuilder get user =>
      _$this._user ??= GGetUserRepositoriesData_userBuilder();
  set user(GGetUserRepositoriesData_userBuilder? user) => _$this._user = user;

  GGetUserRepositoriesDataBuilder() {
    GGetUserRepositoriesData._initializeBuilder(this);
  }

  GGetUserRepositoriesDataBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _user = $v.user?.toBuilder();
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserRepositoriesData other) {
    _$v = other as _$GGetUserRepositoriesData;
  }

  @override
  void update(void Function(GGetUserRepositoriesDataBuilder)? updates) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserRepositoriesData build() => _build();

  _$GGetUserRepositoriesData _build() {
    _$GGetUserRepositoriesData _$result;
    try {
      _$result =
          _$v ??
          _$GGetUserRepositoriesData._(
            G__typename: BuiltValueNullFieldError.checkNotNull(
              G__typename,
              r'GGetUserRepositoriesData',
              'G__typename',
            ),
            user: _user?.build(),
          );
    } catch (_) {
      late String _$failedField;
      try {
        _$failedField = 'user';
        _user?.build();
      } catch (e) {
        throw BuiltValueNestedFieldError(
          r'GGetUserRepositoriesData',
          _$failedField,
          e.toString(),
        );
      }
      rethrow;
    }
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserRepositoriesData_user extends GGetUserRepositoriesData_user {
  @override
  final String G__typename;
  @override
  final GGetUserRepositoriesData_user_repositories repositories;

  factory _$GGetUserRepositoriesData_user([
    void Function(GGetUserRepositoriesData_userBuilder)? updates,
  ]) => (GGetUserRepositoriesData_userBuilder()..update(updates))._build();

  _$GGetUserRepositoriesData_user._({
    required this.G__typename,
    required this.repositories,
  }) : super._();
  @override
  GGetUserRepositoriesData_user rebuild(
    void Function(GGetUserRepositoriesData_userBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserRepositoriesData_userBuilder toBuilder() =>
      GGetUserRepositoriesData_userBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserRepositoriesData_user &&
        G__typename == other.G__typename &&
        repositories == other.repositories;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, repositories.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(r'GGetUserRepositoriesData_user')
          ..add('G__typename', G__typename)
          ..add('repositories', repositories))
        .toString();
  }
}

class GGetUserRepositoriesData_userBuilder
    implements
        Builder<
          GGetUserRepositoriesData_user,
          GGetUserRepositoriesData_userBuilder
        > {
  _$GGetUserRepositoriesData_user? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  GGetUserRepositoriesData_user_repositoriesBuilder? _repositories;
  GGetUserRepositoriesData_user_repositoriesBuilder get repositories =>
      _$this._repositories ??=
          GGetUserRepositoriesData_user_repositoriesBuilder();
  set repositories(
    GGetUserRepositoriesData_user_repositoriesBuilder? repositories,
  ) => _$this._repositories = repositories;

  GGetUserRepositoriesData_userBuilder() {
    GGetUserRepositoriesData_user._initializeBuilder(this);
  }

  GGetUserRepositoriesData_userBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _repositories = $v.repositories.toBuilder();
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserRepositoriesData_user other) {
    _$v = other as _$GGetUserRepositoriesData_user;
  }

  @override
  void update(void Function(GGetUserRepositoriesData_userBuilder)? updates) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserRepositoriesData_user build() => _build();

  _$GGetUserRepositoriesData_user _build() {
    _$GGetUserRepositoriesData_user _$result;
    try {
      _$result =
          _$v ??
          _$GGetUserRepositoriesData_user._(
            G__typename: BuiltValueNullFieldError.checkNotNull(
              G__typename,
              r'GGetUserRepositoriesData_user',
              'G__typename',
            ),
            repositories: repositories.build(),
          );
    } catch (_) {
      late String _$failedField;
      try {
        _$failedField = 'repositories';
        repositories.build();
      } catch (e) {
        throw BuiltValueNestedFieldError(
          r'GGetUserRepositoriesData_user',
          _$failedField,
          e.toString(),
        );
      }
      rethrow;
    }
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserRepositoriesData_user_repositories
    extends GGetUserRepositoriesData_user_repositories {
  @override
  final String G__typename;
  @override
  final BuiltList<GGetUserRepositoriesData_user_repositories_nodes?>? nodes;
  @override
  final GGetUserRepositoriesData_user_repositories_pageInfo pageInfo;

  factory _$GGetUserRepositoriesData_user_repositories([
    void Function(GGetUserRepositoriesData_user_repositoriesBuilder)? updates,
  ]) => (GGetUserRepositoriesData_user_repositoriesBuilder()..update(updates))
      ._build();

  _$GGetUserRepositoriesData_user_repositories._({
    required this.G__typename,
    this.nodes,
    required this.pageInfo,
  }) : super._();
  @override
  GGetUserRepositoriesData_user_repositories rebuild(
    void Function(GGetUserRepositoriesData_user_repositoriesBuilder) updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserRepositoriesData_user_repositoriesBuilder toBuilder() =>
      GGetUserRepositoriesData_user_repositoriesBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserRepositoriesData_user_repositories &&
        G__typename == other.G__typename &&
        nodes == other.nodes &&
        pageInfo == other.pageInfo;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, nodes.hashCode);
    _$hash = $jc(_$hash, pageInfo.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(
            r'GGetUserRepositoriesData_user_repositories',
          )
          ..add('G__typename', G__typename)
          ..add('nodes', nodes)
          ..add('pageInfo', pageInfo))
        .toString();
  }
}

class GGetUserRepositoriesData_user_repositoriesBuilder
    implements
        Builder<
          GGetUserRepositoriesData_user_repositories,
          GGetUserRepositoriesData_user_repositoriesBuilder
        > {
  _$GGetUserRepositoriesData_user_repositories? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  ListBuilder<GGetUserRepositoriesData_user_repositories_nodes?>? _nodes;
  ListBuilder<GGetUserRepositoriesData_user_repositories_nodes?> get nodes =>
      _$this._nodes ??=
          ListBuilder<GGetUserRepositoriesData_user_repositories_nodes?>();
  set nodes(
    ListBuilder<GGetUserRepositoriesData_user_repositories_nodes?>? nodes,
  ) => _$this._nodes = nodes;

  GGetUserRepositoriesData_user_repositories_pageInfoBuilder? _pageInfo;
  GGetUserRepositoriesData_user_repositories_pageInfoBuilder get pageInfo =>
      _$this._pageInfo ??=
          GGetUserRepositoriesData_user_repositories_pageInfoBuilder();
  set pageInfo(
    GGetUserRepositoriesData_user_repositories_pageInfoBuilder? pageInfo,
  ) => _$this._pageInfo = pageInfo;

  GGetUserRepositoriesData_user_repositoriesBuilder() {
    GGetUserRepositoriesData_user_repositories._initializeBuilder(this);
  }

  GGetUserRepositoriesData_user_repositoriesBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _nodes = $v.nodes?.toBuilder();
      _pageInfo = $v.pageInfo.toBuilder();
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserRepositoriesData_user_repositories other) {
    _$v = other as _$GGetUserRepositoriesData_user_repositories;
  }

  @override
  void update(
    void Function(GGetUserRepositoriesData_user_repositoriesBuilder)? updates,
  ) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserRepositoriesData_user_repositories build() => _build();

  _$GGetUserRepositoriesData_user_repositories _build() {
    _$GGetUserRepositoriesData_user_repositories _$result;
    try {
      _$result =
          _$v ??
          _$GGetUserRepositoriesData_user_repositories._(
            G__typename: BuiltValueNullFieldError.checkNotNull(
              G__typename,
              r'GGetUserRepositoriesData_user_repositories',
              'G__typename',
            ),
            nodes: _nodes?.build(),
            pageInfo: pageInfo.build(),
          );
    } catch (_) {
      late String _$failedField;
      try {
        _$failedField = 'nodes';
        _nodes?.build();
        _$failedField = 'pageInfo';
        pageInfo.build();
      } catch (e) {
        throw BuiltValueNestedFieldError(
          r'GGetUserRepositoriesData_user_repositories',
          _$failedField,
          e.toString(),
        );
      }
      rethrow;
    }
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserRepositoriesData_user_repositories_nodes
    extends GGetUserRepositoriesData_user_repositories_nodes {
  @override
  final String G__typename;
  @override
  final String id;
  @override
  final String name;
  @override
  final String nameWithOwner;
  @override
  final String? description;
  @override
  final int stargazerCount;
  @override
  final int forkCount;
  @override
  final GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage?
  primaryLanguage;
  @override
  final _i3.GDateTime updatedAt;

  factory _$GGetUserRepositoriesData_user_repositories_nodes([
    void Function(GGetUserRepositoriesData_user_repositories_nodesBuilder)?
    updates,
  ]) =>
      (GGetUserRepositoriesData_user_repositories_nodesBuilder()
            ..update(updates))
          ._build();

  _$GGetUserRepositoriesData_user_repositories_nodes._({
    required this.G__typename,
    required this.id,
    required this.name,
    required this.nameWithOwner,
    this.description,
    required this.stargazerCount,
    required this.forkCount,
    this.primaryLanguage,
    required this.updatedAt,
  }) : super._();
  @override
  GGetUserRepositoriesData_user_repositories_nodes rebuild(
    void Function(GGetUserRepositoriesData_user_repositories_nodesBuilder)
    updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserRepositoriesData_user_repositories_nodesBuilder toBuilder() =>
      GGetUserRepositoriesData_user_repositories_nodesBuilder()..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserRepositoriesData_user_repositories_nodes &&
        G__typename == other.G__typename &&
        id == other.id &&
        name == other.name &&
        nameWithOwner == other.nameWithOwner &&
        description == other.description &&
        stargazerCount == other.stargazerCount &&
        forkCount == other.forkCount &&
        primaryLanguage == other.primaryLanguage &&
        updatedAt == other.updatedAt;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, id.hashCode);
    _$hash = $jc(_$hash, name.hashCode);
    _$hash = $jc(_$hash, nameWithOwner.hashCode);
    _$hash = $jc(_$hash, description.hashCode);
    _$hash = $jc(_$hash, stargazerCount.hashCode);
    _$hash = $jc(_$hash, forkCount.hashCode);
    _$hash = $jc(_$hash, primaryLanguage.hashCode);
    _$hash = $jc(_$hash, updatedAt.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(
            r'GGetUserRepositoriesData_user_repositories_nodes',
          )
          ..add('G__typename', G__typename)
          ..add('id', id)
          ..add('name', name)
          ..add('nameWithOwner', nameWithOwner)
          ..add('description', description)
          ..add('stargazerCount', stargazerCount)
          ..add('forkCount', forkCount)
          ..add('primaryLanguage', primaryLanguage)
          ..add('updatedAt', updatedAt))
        .toString();
  }
}

class GGetUserRepositoriesData_user_repositories_nodesBuilder
    implements
        Builder<
          GGetUserRepositoriesData_user_repositories_nodes,
          GGetUserRepositoriesData_user_repositories_nodesBuilder
        > {
  _$GGetUserRepositoriesData_user_repositories_nodes? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  String? _id;
  String? get id => _$this._id;
  set id(String? id) => _$this._id = id;

  String? _name;
  String? get name => _$this._name;
  set name(String? name) => _$this._name = name;

  String? _nameWithOwner;
  String? get nameWithOwner => _$this._nameWithOwner;
  set nameWithOwner(String? nameWithOwner) =>
      _$this._nameWithOwner = nameWithOwner;

  String? _description;
  String? get description => _$this._description;
  set description(String? description) => _$this._description = description;

  int? _stargazerCount;
  int? get stargazerCount => _$this._stargazerCount;
  set stargazerCount(int? stargazerCount) =>
      _$this._stargazerCount = stargazerCount;

  int? _forkCount;
  int? get forkCount => _$this._forkCount;
  set forkCount(int? forkCount) => _$this._forkCount = forkCount;

  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder?
  _primaryLanguage;
  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder
  get primaryLanguage => _$this._primaryLanguage ??=
      GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder();
  set primaryLanguage(
    GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder?
    primaryLanguage,
  ) => _$this._primaryLanguage = primaryLanguage;

  _i3.GDateTimeBuilder? _updatedAt;
  _i3.GDateTimeBuilder get updatedAt =>
      _$this._updatedAt ??= _i3.GDateTimeBuilder();
  set updatedAt(_i3.GDateTimeBuilder? updatedAt) =>
      _$this._updatedAt = updatedAt;

  GGetUserRepositoriesData_user_repositories_nodesBuilder() {
    GGetUserRepositoriesData_user_repositories_nodes._initializeBuilder(this);
  }

  GGetUserRepositoriesData_user_repositories_nodesBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _id = $v.id;
      _name = $v.name;
      _nameWithOwner = $v.nameWithOwner;
      _description = $v.description;
      _stargazerCount = $v.stargazerCount;
      _forkCount = $v.forkCount;
      _primaryLanguage = $v.primaryLanguage?.toBuilder();
      _updatedAt = $v.updatedAt.toBuilder();
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserRepositoriesData_user_repositories_nodes other) {
    _$v = other as _$GGetUserRepositoriesData_user_repositories_nodes;
  }

  @override
  void update(
    void Function(GGetUserRepositoriesData_user_repositories_nodesBuilder)?
    updates,
  ) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserRepositoriesData_user_repositories_nodes build() => _build();

  _$GGetUserRepositoriesData_user_repositories_nodes _build() {
    _$GGetUserRepositoriesData_user_repositories_nodes _$result;
    try {
      _$result =
          _$v ??
          _$GGetUserRepositoriesData_user_repositories_nodes._(
            G__typename: BuiltValueNullFieldError.checkNotNull(
              G__typename,
              r'GGetUserRepositoriesData_user_repositories_nodes',
              'G__typename',
            ),
            id: BuiltValueNullFieldError.checkNotNull(
              id,
              r'GGetUserRepositoriesData_user_repositories_nodes',
              'id',
            ),
            name: BuiltValueNullFieldError.checkNotNull(
              name,
              r'GGetUserRepositoriesData_user_repositories_nodes',
              'name',
            ),
            nameWithOwner: BuiltValueNullFieldError.checkNotNull(
              nameWithOwner,
              r'GGetUserRepositoriesData_user_repositories_nodes',
              'nameWithOwner',
            ),
            description: description,
            stargazerCount: BuiltValueNullFieldError.checkNotNull(
              stargazerCount,
              r'GGetUserRepositoriesData_user_repositories_nodes',
              'stargazerCount',
            ),
            forkCount: BuiltValueNullFieldError.checkNotNull(
              forkCount,
              r'GGetUserRepositoriesData_user_repositories_nodes',
              'forkCount',
            ),
            primaryLanguage: _primaryLanguage?.build(),
            updatedAt: updatedAt.build(),
          );
    } catch (_) {
      late String _$failedField;
      try {
        _$failedField = 'primaryLanguage';
        _primaryLanguage?.build();
        _$failedField = 'updatedAt';
        updatedAt.build();
      } catch (e) {
        throw BuiltValueNestedFieldError(
          r'GGetUserRepositoriesData_user_repositories_nodes',
          _$failedField,
          e.toString(),
        );
      }
      rethrow;
    }
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage
    extends GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage {
  @override
  final String G__typename;
  @override
  final String name;
  @override
  final String? color;

  factory _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage([
    void Function(
      GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder,
    )?
    updates,
  ]) =>
      (GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder()
            ..update(updates))
          ._build();

  _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage._({
    required this.G__typename,
    required this.name,
    this.color,
  }) : super._();
  @override
  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage rebuild(
    void Function(
      GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder,
    )
    updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder
  toBuilder() =>
      GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder()
        ..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other
            is GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage &&
        G__typename == other.G__typename &&
        name == other.name &&
        color == other.color;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, name.hashCode);
    _$hash = $jc(_$hash, color.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(
            r'GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage',
          )
          ..add('G__typename', G__typename)
          ..add('name', name)
          ..add('color', color))
        .toString();
  }
}

class GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder
    implements
        Builder<
          GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage,
          GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder
        > {
  _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  String? _name;
  String? get name => _$this._name;
  set name(String? name) => _$this._name = name;

  String? _color;
  String? get color => _$this._color;
  set color(String? color) => _$this._color = color;

  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder() {
    GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage._initializeBuilder(
      this,
    );
  }

  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder
  get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _name = $v.name;
      _color = $v.color;
      _$v = null;
    }
    return this;
  }

  @override
  void replace(
    GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage other,
  ) {
    _$v =
        other
            as _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage;
  }

  @override
  void update(
    void Function(
      GGetUserRepositoriesData_user_repositories_nodes_primaryLanguageBuilder,
    )?
    updates,
  ) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage build() =>
      _build();

  _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage _build() {
    final _$result =
        _$v ??
        _$GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage._(
          G__typename: BuiltValueNullFieldError.checkNotNull(
            G__typename,
            r'GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage',
            'G__typename',
          ),
          name: BuiltValueNullFieldError.checkNotNull(
            name,
            r'GGetUserRepositoriesData_user_repositories_nodes_primaryLanguage',
            'name',
          ),
          color: color,
        );
    replace(_$result);
    return _$result;
  }
}

class _$GGetUserRepositoriesData_user_repositories_pageInfo
    extends GGetUserRepositoriesData_user_repositories_pageInfo {
  @override
  final String G__typename;
  @override
  final bool hasNextPage;
  @override
  final String? endCursor;

  factory _$GGetUserRepositoriesData_user_repositories_pageInfo([
    void Function(GGetUserRepositoriesData_user_repositories_pageInfoBuilder)?
    updates,
  ]) =>
      (GGetUserRepositoriesData_user_repositories_pageInfoBuilder()
            ..update(updates))
          ._build();

  _$GGetUserRepositoriesData_user_repositories_pageInfo._({
    required this.G__typename,
    required this.hasNextPage,
    this.endCursor,
  }) : super._();
  @override
  GGetUserRepositoriesData_user_repositories_pageInfo rebuild(
    void Function(GGetUserRepositoriesData_user_repositories_pageInfoBuilder)
    updates,
  ) => (toBuilder()..update(updates)).build();

  @override
  GGetUserRepositoriesData_user_repositories_pageInfoBuilder toBuilder() =>
      GGetUserRepositoriesData_user_repositories_pageInfoBuilder()
        ..replace(this);

  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is GGetUserRepositoriesData_user_repositories_pageInfo &&
        G__typename == other.G__typename &&
        hasNextPage == other.hasNextPage &&
        endCursor == other.endCursor;
  }

  @override
  int get hashCode {
    var _$hash = 0;
    _$hash = $jc(_$hash, G__typename.hashCode);
    _$hash = $jc(_$hash, hasNextPage.hashCode);
    _$hash = $jc(_$hash, endCursor.hashCode);
    _$hash = $jf(_$hash);
    return _$hash;
  }

  @override
  String toString() {
    return (newBuiltValueToStringHelper(
            r'GGetUserRepositoriesData_user_repositories_pageInfo',
          )
          ..add('G__typename', G__typename)
          ..add('hasNextPage', hasNextPage)
          ..add('endCursor', endCursor))
        .toString();
  }
}

class GGetUserRepositoriesData_user_repositories_pageInfoBuilder
    implements
        Builder<
          GGetUserRepositoriesData_user_repositories_pageInfo,
          GGetUserRepositoriesData_user_repositories_pageInfoBuilder
        > {
  _$GGetUserRepositoriesData_user_repositories_pageInfo? _$v;

  String? _G__typename;
  String? get G__typename => _$this._G__typename;
  set G__typename(String? G__typename) => _$this._G__typename = G__typename;

  bool? _hasNextPage;
  bool? get hasNextPage => _$this._hasNextPage;
  set hasNextPage(bool? hasNextPage) => _$this._hasNextPage = hasNextPage;

  String? _endCursor;
  String? get endCursor => _$this._endCursor;
  set endCursor(String? endCursor) => _$this._endCursor = endCursor;

  GGetUserRepositoriesData_user_repositories_pageInfoBuilder() {
    GGetUserRepositoriesData_user_repositories_pageInfo._initializeBuilder(
      this,
    );
  }

  GGetUserRepositoriesData_user_repositories_pageInfoBuilder get _$this {
    final $v = _$v;
    if ($v != null) {
      _G__typename = $v.G__typename;
      _hasNextPage = $v.hasNextPage;
      _endCursor = $v.endCursor;
      _$v = null;
    }
    return this;
  }

  @override
  void replace(GGetUserRepositoriesData_user_repositories_pageInfo other) {
    _$v = other as _$GGetUserRepositoriesData_user_repositories_pageInfo;
  }

  @override
  void update(
    void Function(GGetUserRepositoriesData_user_repositories_pageInfoBuilder)?
    updates,
  ) {
    if (updates != null) updates(this);
  }

  @override
  GGetUserRepositoriesData_user_repositories_pageInfo build() => _build();

  _$GGetUserRepositoriesData_user_repositories_pageInfo _build() {
    final _$result =
        _$v ??
        _$GGetUserRepositoriesData_user_repositories_pageInfo._(
          G__typename: BuiltValueNullFieldError.checkNotNull(
            G__typename,
            r'GGetUserRepositoriesData_user_repositories_pageInfo',
            'G__typename',
          ),
          hasNextPage: BuiltValueNullFieldError.checkNotNull(
            hasNextPage,
            r'GGetUserRepositoriesData_user_repositories_pageInfo',
            'hasNextPage',
          ),
          endCursor: endCursor,
        );
    replace(_$result);
    return _$result;
  }
}

// ignore_for_file: deprecated_member_use_from_same_package,type=lint
