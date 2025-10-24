# PowerShell script to fix config.yaml
# Run this in your PowerShell terminal

# 1. Backup original file
Copy-Item config/config.yaml config/config.yaml.backup
Write-Host "✅ Backup created: config/config.yaml.backup" -ForegroundColor Green

# 2. Create fixed config.yaml
@"
# Game Bot Configuration
bot:
  name: "GameBot AutoRohan"
  version: "1.0.0"
  debug_mode: false
  log_level: "INFO"

# Window settings
window:
  title: "Rohan"
  capture_mode: "window"
  focus_on_start: true

# Screen detection settings
screen:
  resolution: [1920, 1080]
  capture_fps: 30
  template_match_threshold: 0.8

# Player action settings
player:
  attack_key: "1"
  skill_keys: ["2", "3", "4", "5"]
  potion_key: "F1"
  auto_pickup: true
  pickup_radius: 100

# Bot behavior
behavior:
  auto_attack: true
  auto_skill: true
  auto_potion: true
  potion_hp_threshold: 50
  rest_after_kill: 1.0

# Hotkeys
hotkeys:
  start: "F9"
  stop: "F10"
  pause: "F11"
  emergency_stop: "F12"

# Safety settings
safety:
  max_runtime_minutes: 180
  screenshot_on_error: true
  auto_stop_on_death: true
"@ | Out-File -FilePath config/config.yaml -Encoding utf8

Write-Host "✅ Fixed config.yaml created" -ForegroundColor Green

# 3. Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config/config.yaml')); print('✅ YAML syntax is valid')"

# 4. Show the file
Write-Host "`n📄 New config.yaml content:" -ForegroundColor Cyan
Get-Content config/config.yaml
