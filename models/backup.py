import os
import zipfile
import logging
import shutil

from datetime import datetime
from dataclasses import dataclass
from models.when import When

logger = logging.getLogger()

@dataclass
class Backup:
    name: str  # name to call the backup
    backup_from: str  # path to backup from
    backup_to: str  # path to backup to
    when: When  # when to backup

    @property
    def backup_from_directory(self) -> bool:
        return os.path.isdir(self.backup_from)

    @property
    def backup_to_directory(self) -> bool:
        return os.path.isdir(self.backup_to)

    def paths_exist(self) -> bool:
        """ checks if both backup paths exist """
        return all([
            os.path.exists(self.backup_from),
            os.path.exists(self.backup_to)
        ])

    def get_new_file_name(self) -> str:
        """ returns a new name of the zipped file"""
        return f'{self.name}_{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.zip'

    def zip_dir(self, zip_file_name) -> str:
        
        backup_to = f"{'/'.join(self.backup_from.split('/')[:-1])}\{zip_file_name}"
        logger.info("starting directory backup")
        with zipfile.ZipFile(backup_to, mode='w', compression=zipfile.ZIP_DEFLATED) as archive:
            for root, dirs, files in os.walk(self.backup_from):
                for file in files:
                    logger.info("backing up: %s to %s" % (file, backup_to))
                    archive.write(os.path.join(root, file),
                                  os.path.relpath(os.path.join(root, file),
                                                  os.path.join(backup_to, '..')))
        return backup_to

    def zip_file(self, zip_file_name: str):
        backup_to = f"{'/'.join(self.backup_from.split('/')[:-1])}\{zip_file_name}"
        with zipfile.ZipFile(backup_to, mode='w', compression=zipfile.ZIP_DEFLATED) as archive:
            logger.info("backing up file: %s to %s" % (self.backup_from, backup_to))
            archive.write(self.backup_from)  

    def move_file(self, location: str):
        """ moves a file from a location to the destination """
        logger.info("moving zip to final location")
        shutil.move(location, self.backup_to)

    def backup(self):
        if not self.paths_exist():
            raise ValueError("Both backup paths must exist:")    
        
        if not self.backup_to_directory:
            raise NotADirectoryError("You can only backup to a directory")

        zipped_file_name = self.get_new_file_name()

        if self.backup_from_directory:
            location = self.zip_dir(zipped_file_name)
        else:
            location = self.zip_file(zipped_file_name)

        self.move_file(location)
