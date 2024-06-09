# Expose the Docker API for remote development in PyCharm

- Locate the docker service using `sudo find /etc/systemd/system/ -name docker.service`
- Edit the display file. Ex: `sudo nano /etc/systemd/system/multi-user.target.wants/docker.service`
- Locate the line starting with "ExecStart" and add the option `-H tcp://0.0.0.0:2375` at the end. 
  - Ex: `ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock -H tcp://0.0.0.0:2375`
- Save the file and reload the daemon units: `systemctl daemon-reload`
- Restart the Docker service: `sudo systemctl restart docker`
- Connect to the daemon remotely in PyCharm
  - Navigate to `Tools` > `Services` > `Docker` > `Connection`
  - Choose "TCP socket" and enter the host:port. Ex: `tcp://influxdb.local:2375` 
  - You should see "Connection successful" at the bottom of the window

### Troubleshooting
- Use the command `sudo journalctl -u docker` to view the Docker engine service logs.
- `sudo netstat -tlnp` Should display a listening service on 2375. Ex: `tcp6       0      0 :::2375                 :::*                    LISTEN      27926/dockerd`