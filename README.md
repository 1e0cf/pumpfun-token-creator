# Installation
## 1. Install uv
https://docs.astral.sh/uv/getting-started/installation/
## 2. Install dependencies
```
uv sync
```
## 3. Edit config
```
cp config.example.yaml config.yaml
```
Edit config.yaml
## 4. Create metadata file
```
cp metadata.example.yaml metadata.yaml
```
Paste here metadata for your tokens
## 5. Create signers file
```
touch signers.txt
```
Paste your private keys in base58 format here. One per line.

# Usage
```
uv run main.py
```
