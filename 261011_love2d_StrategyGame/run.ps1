param([string]$LovePath = 'C:\설치_soft\260817_Code\LOVE\love.exe')
if (-not (Test-Path -LiteralPath $LovePath -PathType Leaf)) {
    $command = Get-Command love -ErrorAction SilentlyContinue
    if ($command) { $LovePath = $command.Source }
    else { throw 'LÖVE 실행 파일을 찾을 수 없습니다. -LovePath 매개변수로 경로를 지정하세요.' }
}
& $LovePath $PSScriptRoot
