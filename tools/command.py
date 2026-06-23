import subprocess

def run_command(cmd):

    forbidden = [
        "rm -rf",
        "mkfs",
        ":(){ :|:& };:"
    ]

    if any(x in cmd for x in forbidden):
        return "Command blocked for security reasons."

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return str(e)