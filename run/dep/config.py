import yaml
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    host: str
    username: Optional[str]
    password: Optional[str]
    bin_file: str
    test_folder: Optional[str]
    script_file: Optional[str]
    destination_folder: Optional[str]

    @classmethod
    def from_yaml(cls, file_path: str) -> 'Config':
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        return cls(
            host=data['host'],
            username=data.get('username'),
            password=data.get('password'),
            bin_file=data['bin_file'],
            test_folder=data.get('test_folder'),
            script_file=data.get('script_file'),
            destination_folder=data.get('destination_folder')
        )

    def get_connection_type(self) -> str:
        connection_type = 'local' if self.host == 'local' else 'ssh'
        return connection_type

    def get_run_cmd(self) -> str :
        if self.get_connection_type() == 'local':
            command = f"pwd && chmod +x {self.test_folder}/{self.script_file} " \
                    f"&& {self.test_folder}/{self.script_file} {self.bin_file}"
        else:
            command = f"chmod +x {self.destination_folder}/{self.script_file} " \
                    f"&& {self.destination_folder}/{self.script_file} {self.bin_file} {self.password}"

        return command
