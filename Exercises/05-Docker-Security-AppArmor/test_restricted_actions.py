
import docker
import time

client = docker.from_env()
container = None

try:
    print("Starting restricted-action test...")

    container = client.containers.run(
        "flask-apparmor",
        detach=True,
        security_opt=["apparmor=my-apparmor-profile"],
        command=["python", "-c", "import time; time.sleep(120)"]
    )

    print("Container started:", container.short_id)
    container.reload()
    print("Status:", container.status)

    tests = [
        (
            "Read /etc/passwd",
            ["python", "-c",
             "open('/etc/passwd').read(); print('Read succeeded')"]
        ),
        (
            "Execute /bin/bash",
            ["/bin/bash", "-c", "echo Bash executed"]
        )
    ]

    for name, command in tests:
        print(f"\nTesting: {name}")

        result = container.exec_run(command)

        print("Exit code:", result.exit_code)
        print(result.output.decode(errors="replace"))

        if result.exit_code != 0:
            print("Action failed; check AppArmor logs to confirm the cause.")
        else:
            print("Action succeeded.")

finally:
    if container is not None:
        try:
            container.stop(timeout=5)
            print("\nTest container stopped.")
        except Exception as error:
            print("\nCould not stop test container:", error)
