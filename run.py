import time
import logging
from services.backup_service import BackupService
from services.running_process_service import check_if_running_process

logging.basicConfig(filename='backups.log', encoding='utf-8', level=logging.INFO)

service = BackupService("backups.json")

was_running_minecraft = False

while True:
    time.sleep(20)
    running_minecraft = check_if_running_process("minecraft")
    if not running_minecraft and was_running_minecraft:
        for backup in service.backups:
            backup.backup()
    was_running_minecraft = running_minecraft
