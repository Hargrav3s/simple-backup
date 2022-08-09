from dataclasses import dataclass
import json
import logging

from models import Backups, Backup
from models.when import When

logger = logging.getLogger()


@dataclass
class BackupService:
    path_to_backups_json: str
    backups: list[Backup]

    def __init__(self, path_to_backups_json):
        self.path_to_backups_json = path_to_backups_json
        logger.info(f"loading json {path_to_backups_json}")
    
        with open(self.path_to_backups_json) as json_file:
            backups_json = json.load(json_file)
        
        self.backups = [Backup(**backup) for backup in Backups(**backups_json).backups]

        for backup in self.backups:
            backup.when = When(**backup.when)

    def do_backups(self):
        for backup in self.backups:
            logger.info(f"Running backup {backup.name}")
            backup.backup()

if __name__ == "__main__":
    service = BackupService()
    print(service)
