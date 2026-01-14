#!/bin/bash

# Script para renomear arquivo para uso com Docker (Linux/Mac)
# Este script permite selecionar um arquivo Excel e renomeá-lo para um padrão

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_DIR="$SCRIPT_DIR/content"

if [ ! -d "$CONTENT_DIR" ]; then
    echo "Pasta 'content' não encontrada!"
    exit 1
fi

# Se passou arquivo como argumento, usa esse
if [ -n "$1" ]; then
    SELECTED_FILE="$1"
    if [ ! -f "$SELECTED_FILE" ]; then
        echo "Arquivo não encontrado: $SELECTED_FILE"
        exit 1
    fi
else
    # Tenta usar zenity (GUI) se disponível
    if command -v zenity &> /dev/null; then
        SELECTED_FILE=$(zenity --file-selection --title="Selecione o arquivo Excel para processar" --file-filter="*.xlsx *.xls" 2>/dev/null)
        if [ -z "$SELECTED_FILE" ]; then
            echo "Nenhum arquivo selecionado."
            exit 1
        fi
    else
        # Fallback: mostrar arquivos na pasta content e pedir seleção
        echo "Arquivos .xlsx ou .xsl encontrados em ./content:"
        ls -1 "$CONTENT_DIR"/*.xlsx "$CONTENT_DIR"/*.xls 2>/dev/null || echo "Nenhum arquivo encontrado"
        echo ""
        read -p "Digite o caminho completo do arquivo (ou nome se estiver em ./content): " SELECTED_FILE
        
        if [ ! -f "$SELECTED_FILE" ]; then
            SELECTED_FILE="$CONTENT_DIR/$SELECTED_FILE"
            if [ ! -f "$SELECTED_FILE" ]; then
                echo "Arquivo não encontrado!"
                exit 1
            fi
        fi
    fi
fi

FILE_NAME=$(basename "$SELECTED_FILE")
echo ""
echo "✅ Arquivo selecionado: $FILE_NAME"

# Renomear arquivo para padrão
NEW_PATH="$CONTENT_DIR/input.xlsx"

# Se já existe um arquivo input.xlsx, fazer backup
if [ -f "$NEW_PATH" ]; then
    BACKUP_PATH="$CONTENT_DIR/input_backup_$(date +%Y%m%d_%H%M%S).xlsx"
    mv "$NEW_PATH" "$BACKUP_PATH"
    echo "Backup anterior salvo como: $(basename $BACKUP_PATH)"
fi

# Copiar arquivo selecionado
cp "$SELECTED_FILE" "$NEW_PATH"
echo "Arquivo padronizado como: input.xlsx"

echo ""
echo "Você pode agora rodar o Docker:"
echo "   docker-compose up"
