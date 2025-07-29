import subprocess
import sys
from typing import List, Optional


def run_command_realtime(command: List[str], cwd: Optional[str] = None) -> int:
    """
    Run a command and print its output in real-time

    Args:
        command: List of command and arguments (e.g., ['ls', '-la'])
        cwd: Working directory for the command (optional)

    Returns:
        Exit code of the process
    """
    try:
        print(f"Running command: {' '.join(command)}")
        if cwd:
            print(f"Working directory: {cwd}")
        print("-" * 50)

        # Start the process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr with stdout
            universal_newlines=True,
            bufsize=1,  # Line buffered
            cwd=cwd
        )

        # Read and print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.rstrip())  # Print without extra newlines
                sys.stdout.flush()  # Ensure immediate output

        # Wait for process to complete
        exit_code = process.wait()

        print("-" * 50)
        print(f"Process completed with exit code: {exit_code}")

        return exit_code

    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        if process:
            process.terminate()
            process.wait()
        return 130
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found")
        return 127
    except Exception as e:
        print(f"Error running command: {e}")
        return 1


commands = [
    # Test with a simple command
    ["echo", "Hello, World!"],

    # Test with a command that produces output over time
    ["ping", "-n", "5", "8.8.8.8"],

    # Uncomment to test with a Python script
    # ["python3", "-c", "import time; [print(f'Line {i}') or time.sleep(1) for i in range(5)]"],

    # Uncomment to test with a shell command that takes time
    # ["bash", "-c", "for i in {1..5}; do echo 'Count: $i'; sleep 1; done"],
]

for cmd in commands:
    exit_code = run_command_realtime(cmd)
    print(f"exit code = {exit_code}")