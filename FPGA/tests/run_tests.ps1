param([Parameter(Mandatory=$true)][string]$IverilogBin)
$ErrorActionPreference='Stop'
$prior=Get-Location
try {
 Set-Location (Split-Path $PSScriptRoot -Parent)
 $rtl=@('src/ear_training.v','src/pcm5102_i2s_tx.v','src/ads1115_pressure_test.v','src/additive32_bank.v','src/dpg_uart.v','src/dpg_bridge.v','src/oled_audio_scope.v','src/oled_i2c_byte.v')
 $tests=@(@('bank','tb_bank'),@('guitar_control','tb_guitar_control'),@('phone_game','tb_phone_game'),@('bend_top','tb_bend_top'),@('modes','tb_tjc_modes'),@('integration','tb_integration'),@('pcm5102_i2s','tb_pcm5102_i2s'),@('pcm5102_integration','tb_pcm5102_integration'),@('game_stats','tb_game_stats'),@('ear','tb_ear'),@('ear_top','tb_ear_top'))
 foreach($test in $tests){
  $name=$test[0];$top=$test[1];$extra=@()
  if($name -eq 'guitar_control'){$extra=@('tests/donor_voice.v')}
  if($name -like 'pcm5102*'){$extra=@('tests/i2s_checker.v')}
  & (Join-Path $IverilogBin 'iverilog.exe') -g2001 -s $top -o "tests/$name.vvp" "tests/tb_$name.v" @extra @rtl
  if($LASTEXITCODE -ne 0){throw "compile failed: $name"}
  & (Join-Path $IverilogBin 'vvp.exe') "tests/$name.vvp" | Tee-Object "validation/$name.log"
  if($LASTEXITCODE -ne 0){throw "simulation failed: $name"}
 }
} finally {Set-Location $prior}

