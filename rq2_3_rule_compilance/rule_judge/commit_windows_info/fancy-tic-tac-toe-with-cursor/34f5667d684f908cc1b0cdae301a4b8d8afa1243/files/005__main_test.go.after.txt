package main

import "testing"

func TestGetGreeting(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "default greeting",
			input:    "",
			expected: "Hello, World!",
		},
		{
			name:     "custom greeting",
			input:    "All",
			expected: "Hello, All!",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getGreeting(tt.input)
			if result != tt.expected {
				t.Errorf("Expected %q but got %q", tt.expected, result)
			}
		})
	}
}
