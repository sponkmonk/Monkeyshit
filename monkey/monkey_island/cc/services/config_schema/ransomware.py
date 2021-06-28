RANSOMWARE = {
    "title": "Ransomware",
    "type": "object",
    "properties": {
        "directories": {
            "title": "Directories to encrypt",
            "type": "object",
            "properties": {
                "linux_dir": {
                    "title": "Linux encryptable directory",
                    "type": "string",
                    "default": "",
                    "description": "Files in the specified directory will be encrypted "
                    "using bitflip to simulate ransomware.",
                },
                "windows_dir": {
                    "title": "Windows encryptable directory",
                    "type": "string",
                    "default": "",
                    "description": "Files in the specified directory will be encrypted "
                    "using bitflip to simulate ransomware.",
                },
            },
        },
        "other_behaviors": {
            "title": "Other Behaviors",
            "type": "object",
            "properties": {
                "readme": {
                    "title": "Create a README.TXT file",
                    "type": "boolean",
                    "default": True,
                    "description": "Creates a README.txt ransomware note on infected systems.",
                }
            },
        },
    },
}
