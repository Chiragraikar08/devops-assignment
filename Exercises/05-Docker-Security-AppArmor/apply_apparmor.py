
import docker

client = docker.from_env()

print("Building Docker image...")
client.images.build(path=".", tag="flask-apparmor")

container = None

try:
    print("Starting container with AppArmor...")
    container = client.containers.run(
        "flask-apparmor",
        ports={"5000/tcp": 5001},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True
    )

    info = client.api.inspect_container(container.id)

    print("Container started:", container.short_id)
    print("AppArmor security options:",
          info["HostConfig"]["SecurityOpt"])

finally:
    if container is not None:
        container.stop()
        container.remove()
        print("Container stopped and removed.")
