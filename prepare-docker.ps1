# Script para renomear arquivo inserido no content para uso no Docker

Add-Type -AssemblyName System.Windows.Forms

$folderPath = "$PSScriptRoot\content"

if (-not (Test-Path $folderPath)) {
    Write-Host "Pasta 'content' não encontrada!" -ForegroundColor Red
    exit 1
}

$openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$openFileDialog.Title = "Selecione o arquivo Excel para processar"
$openFileDialog.Filter = "Arquivos Excel (*.xlsx;*.xls)|*.xlsx;*.xls|Todos os arquivos (*.*)|*.*"
$openFileDialog.InitialDirectory = $folderPath

if ($openFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $selectedFile = $openFileDialog.FileName
    $fileName = Split-Path $selectedFile -Leaf
    
    Write-Host "`n Arquivo selecionado: $fileName" -ForegroundColor Green
    
    # Renomear arquivo para padrão
    $newPath = Join-Path $folderPath "input.xlsx"
    
    # Se já existe um arquivo input.xlsx, fazer backup
    if (Test-Path $newPath) {
        $backupPath = Join-Path $folderPath "input_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').xlsx"
        Rename-Item -Path $newPath -NewName $backupPath -Force
        Write-Host "Backup anterior salvo como: $(Split-Path $backupPath -Leaf)" -ForegroundColor Yellow
    }
    
    # Renomear arquivo selecionado
    Copy-Item -Path $selectedFile -Destination $newPath -Force
    Write-Host "Arquivo padronizado como: input.xlsx" -ForegroundColor Green
    
    Write-Host "`n Você pode agora rodar o Docker:" -ForegroundColor Cyan
    Write-Host "   docker-compose up" -ForegroundColor Cyan
    Write-Host "`nOu manualmente:" -ForegroundColor Cyan
    Write-Host "   docker run -v `$(pwd)/content:/app/content scrapping-empresas python -m src.main content/input.xlsx" -ForegroundColor Cyan
} else {
    Write-Host "Nenhum arquivo selecionado." -ForegroundColor Red
}
