// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint

// ignore_for_file: no_leading_underscores_for_library_prefixes
import 'package:gh3/src/widgets/repository_card/__generated__/repository_card.ast.gql.dart'
    as _i3;
import 'package:gh3/src/widgets/user_profile/__generated__/user_profile.ast.gql.dart'
    as _i2;
import 'package:gql/ast.dart' as _i1;

const GetUserDetails = _i1.OperationDefinitionNode(
  type: _i1.OperationType.query,
  name: _i1.NameNode(value: 'GetUserDetails'),
  variableDefinitions: [
    _i1.VariableDefinitionNode(
      variable: _i1.VariableNode(name: _i1.NameNode(value: 'login')),
      type: _i1.NamedTypeNode(
        name: _i1.NameNode(value: 'String'),
        isNonNull: true,
      ),
      defaultValue: _i1.DefaultValueNode(value: null),
      directives: [],
    ),
  ],
  directives: [],
  selectionSet: _i1.SelectionSetNode(
    selections: [
      _i1.FieldNode(
        name: _i1.NameNode(value: 'user'),
        alias: null,
        arguments: [
          _i1.ArgumentNode(
            name: _i1.NameNode(value: 'login'),
            value: _i1.VariableNode(name: _i1.NameNode(value: 'login')),
          ),
        ],
        directives: [],
        selectionSet: _i1.SelectionSetNode(
          selections: [
            _i1.FragmentSpreadNode(
              name: _i1.NameNode(value: 'UserProfileFragment'),
              directives: [],
            ),
          ],
        ),
      ),
    ],
  ),
);
const GetUserRepositories = _i1.OperationDefinitionNode(
  type: _i1.OperationType.query,
  name: _i1.NameNode(value: 'GetUserRepositories'),
  variableDefinitions: [
    _i1.VariableDefinitionNode(
      variable: _i1.VariableNode(name: _i1.NameNode(value: 'login')),
      type: _i1.NamedTypeNode(
        name: _i1.NameNode(value: 'String'),
        isNonNull: true,
      ),
      defaultValue: _i1.DefaultValueNode(value: null),
      directives: [],
    ),
    _i1.VariableDefinitionNode(
      variable: _i1.VariableNode(name: _i1.NameNode(value: 'first')),
      type: _i1.NamedTypeNode(
        name: _i1.NameNode(value: 'Int'),
        isNonNull: true,
      ),
      defaultValue: _i1.DefaultValueNode(value: null),
      directives: [],
    ),
    _i1.VariableDefinitionNode(
      variable: _i1.VariableNode(name: _i1.NameNode(value: 'after')),
      type: _i1.NamedTypeNode(
        name: _i1.NameNode(value: 'String'),
        isNonNull: false,
      ),
      defaultValue: _i1.DefaultValueNode(value: null),
      directives: [],
    ),
  ],
  directives: [],
  selectionSet: _i1.SelectionSetNode(
    selections: [
      _i1.FieldNode(
        name: _i1.NameNode(value: 'user'),
        alias: null,
        arguments: [
          _i1.ArgumentNode(
            name: _i1.NameNode(value: 'login'),
            value: _i1.VariableNode(name: _i1.NameNode(value: 'login')),
          ),
        ],
        directives: [],
        selectionSet: _i1.SelectionSetNode(
          selections: [
            _i1.FieldNode(
              name: _i1.NameNode(value: 'repositories'),
              alias: null,
              arguments: [
                _i1.ArgumentNode(
                  name: _i1.NameNode(value: 'first'),
                  value: _i1.VariableNode(name: _i1.NameNode(value: 'first')),
                ),
                _i1.ArgumentNode(
                  name: _i1.NameNode(value: 'after'),
                  value: _i1.VariableNode(name: _i1.NameNode(value: 'after')),
                ),
                _i1.ArgumentNode(
                  name: _i1.NameNode(value: 'orderBy'),
                  value: _i1.ObjectValueNode(
                    fields: [
                      _i1.ObjectFieldNode(
                        name: _i1.NameNode(value: 'field'),
                        value: _i1.EnumValueNode(
                          name: _i1.NameNode(value: 'UPDATED_AT'),
                        ),
                      ),
                      _i1.ObjectFieldNode(
                        name: _i1.NameNode(value: 'direction'),
                        value: _i1.EnumValueNode(
                          name: _i1.NameNode(value: 'DESC'),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              directives: [],
              selectionSet: _i1.SelectionSetNode(
                selections: [
                  _i1.FieldNode(
                    name: _i1.NameNode(value: 'nodes'),
                    alias: null,
                    arguments: [],
                    directives: [],
                    selectionSet: _i1.SelectionSetNode(
                      selections: [
                        _i1.FragmentSpreadNode(
                          name: _i1.NameNode(value: 'RepositoryCardFragment'),
                          directives: [],
                        ),
                      ],
                    ),
                  ),
                  _i1.FieldNode(
                    name: _i1.NameNode(value: 'pageInfo'),
                    alias: null,
                    arguments: [],
                    directives: [],
                    selectionSet: _i1.SelectionSetNode(
                      selections: [
                        _i1.FieldNode(
                          name: _i1.NameNode(value: 'hasNextPage'),
                          alias: null,
                          arguments: [],
                          directives: [],
                          selectionSet: null,
                        ),
                        _i1.FieldNode(
                          name: _i1.NameNode(value: 'endCursor'),
                          alias: null,
                          arguments: [],
                          directives: [],
                          selectionSet: null,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ],
  ),
);
const document = _i1.DocumentNode(
  definitions: [
    GetUserDetails,
    GetUserRepositories,
    _i2.UserProfileFragment,
    _i3.RepositoryCardFragment,
  ],
);
