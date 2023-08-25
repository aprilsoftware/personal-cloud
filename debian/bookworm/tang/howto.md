# Install tang

    apt install tang

# Commands
Bind

    clevis luks bind -d /dev/nvme1n1 tang '{"url":"http://192.168.0.2"}'

Unbind

    clevis luks unbind -d /dev/nvme1n1 -s 1
