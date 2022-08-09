from dataclasses import dataclass
from models.backup import Backup

@dataclass
class Backups:
    backups: list[Backup]
