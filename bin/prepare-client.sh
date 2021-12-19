#!/bin/bash

mkdir static

cd ./client && pnpm install && pnpm run build && mv ./build/** ../static
