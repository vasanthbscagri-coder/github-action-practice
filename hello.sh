#!/bin/bash

echo "Hello from GitHub Actions!"
echo "Current date: $(date)"

a=10
b=20
result=$((a + b))

echo "Result: $result"

if [ "$result" -eq 3 ]; then
    echo "Test passed!"
else
    echo "Test failed!"
    exit 1
fi