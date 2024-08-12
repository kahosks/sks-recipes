import os
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["IntunePackager"]

class IntunePackager(Processor):
    input_variables = {
        "source_path": {
            "required": True,
            "description": "The path to the package to be packaged.",
        },
        "destination_path": {
            "required": True,
            "description": "The directory where the package will be saved to.",
        },
        "setup_file": {
            "required": True,
            "description": "The setup file to be packaged.",
        },
        "powershell_path": {
            "required": True,
            "description": "The path to the powershell executable.",
        },  
    }
    output_variables = {
        "intunewin_path": {
            "description": "The path to the packaged intunewin.",
        },
    }

    def main(self):
        try:
            os.makedirs(self.env.get("destination_path"), exist_ok=True)
            r = subprocess.Popen([self.env.get("powershell_path"), "IntuneProcessors/intune-package-win32.ps1", self.env.get("source_path"), self.env.get("destination_path"), self.env.get("setup_file")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(r.stdout.read().decode().strip())
            file_name = self.env.get("destination_path") + "/" + self.env.get("setup_file").replace(".exe", ".intunewin")
            print(file_name)
            if (os.path.exists(file_name)) is True:
                print("File created @ " + file_name)
                self.env["intunewin_path"] = file_name
            else:
                raise ProcessorError("Packaging failed, intunewin not created")
        except Exception as err:
            raise ProcessorError(err)
        
if __name__ == "__main__":
    PROCESSOR = IntunePackager()
    PROCESSOR.execute_shell()
