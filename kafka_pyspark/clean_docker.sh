#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Removing all containers"
docker rm -f $(docker ps -aq)

echo "Stopping and removing containers, networks, and volumes..."
docker-compose down -v --remove-orphans

echo "Pruning all unused volumes..."
docker volume prune --all -f

echo "Pruning all build cache..."
docker builder prune --all -f

echo "Pruning all unused images..."
docker image prune --all -f

echo "Removing volume directories..."
rm -rf kafka0_data kafka1_data kafka2_data

echo "Docker cleanup complete."
