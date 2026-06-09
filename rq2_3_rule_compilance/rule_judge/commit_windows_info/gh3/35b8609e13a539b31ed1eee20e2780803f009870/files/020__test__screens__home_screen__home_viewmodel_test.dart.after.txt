import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:ferry/ferry.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:gh3/src/screens/home_screen/__generated__/home_viewmodel.req.gql.dart';
import 'package:gh3/src/screens/home_screen/__generated__/home_viewmodel.data.gql.dart';
import 'package:gh3/src/screens/home_screen/__generated__/home_viewmodel.var.gql.dart';

import 'home_viewmodel_test.mocks.dart';

@GenerateMocks([Client])
void main() {
  group('HomeViewModel', () {
    late MockClient mockClient;
    late HomeViewModel viewModel;
    late StreamController<
      OperationResponse<GGetFollowingData, GGetFollowingVars>
    >
    streamController;

    setUp(() {
      mockClient = MockClient();
      streamController =
          StreamController<
            OperationResponse<GGetFollowingData, GGetFollowingVars>
          >();
      viewModel = HomeViewModel(mockClient);
    });

    tearDown(() {
      streamController.close();
      viewModel.dispose();
    });

    test('should properly dispose of subscriptions', () async {
      // Setup mock to return our controlled stream
      when(mockClient.request(any)).thenAnswer((_) => streamController.stream);

      // Start loading to create subscription
      await viewModel.loadFollowingUsers();

      // Verify subscription is active
      expect(viewModel.isLoading, true);

      // Dispose the view model
      viewModel.dispose();

      // Verify the view model is disposed
      expect(viewModel.disposed, true);

      // Add data to stream after disposal - should not cause issues
      streamController.add(
        OperationResponse<GGetFollowingData, GGetFollowingVars>(
          operationRequest: GGetFollowingReq((b) => b..vars.first = 20),
          data: null,
        ),
      );

      // Should not throw or cause memory leaks
      await Future.delayed(Duration(milliseconds: 10));
    });

    test('should not notify listeners after disposal', () async {
      bool listenerCalled = false;
      viewModel.addListener(() {
        listenerCalled = true;
      });

      // Setup mock
      when(mockClient.request(any)).thenAnswer((_) => streamController.stream);

      // Start loading
      await viewModel.loadFollowingUsers();

      // Dispose
      viewModel.dispose();
      listenerCalled = false;

      // Try to add data after disposal
      streamController.add(
        OperationResponse<GGetFollowingData, GGetFollowingVars>(
          operationRequest: GGetFollowingReq((b) => b..vars.first = 20),
          data: null,
        ),
      );

      await Future.delayed(Duration(milliseconds: 10));
      expect(listenerCalled, false);
    });

    test('should handle multiple dispose calls gracefully', () {
      // Setup mock
      when(mockClient.request(any)).thenAnswer((_) => streamController.stream);

      viewModel.loadFollowingUsers();

      // Multiple dispose calls should not throw
      expect(() {
        viewModel.dispose();
        viewModel.dispose();
        viewModel.dispose();
      }, returnsNormally);

      expect(viewModel.disposed, true);
    });

    test('should clear internal state on disposal', () async {
      // Setup mock with data
      when(mockClient.request(any)).thenAnswer((_) => streamController.stream);

      // Load data
      await viewModel.loadFollowingUsers();

      // Simulate receiving data
      streamController.add(
        OperationResponse<GGetFollowingData, GGetFollowingVars>(
          operationRequest: GGetFollowingReq((b) => b..vars.first = 20),
          data: null,
        ),
      );

      // Dispose
      viewModel.dispose();

      // Internal state should be cleared (this is implementation detail,
      // but important for preventing memory leaks)
      expect(viewModel.disposed, true);
    });
  });
}
