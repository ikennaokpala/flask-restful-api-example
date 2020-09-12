resource "openstack_compute_floatingip_associate_v2" "floating_ip" {
  floating_ip = data.openstack_networking_floatingip_v2.floating_ip.address
  fixed_ip = data.openstack_networking_floatingip_v2.floating_ip.fixed_ip
  instance_id = openstack_compute_instance_v2.rdb-vm.id
}

provider "openstack" {
  cloud   = var.os_cloud
  user_name   = var.user_name
  password   = var.password
  tenant_name = var.os_tenant_name
  tenant_id   = var.os_tenant_id
  auth_url    = var.os_auth_url
}

# Launch instance
resource "openstack_compute_instance_v2" "rdb-vm" {
	name = "rdb-${var.environment}-vm"
	image_id = var.image["id"]
	flavor_id = var.flavor["id"]
	key_pair = "${var.dev_ssh_key_name}-rdb-prod"
	security_groups = ["${openstack_compute_secgroup_v2.rdb-security-group.id}"]
	network {
		uuid = var.private["id"]
	}
  
	# Install system in volume
  block_device {
    volume_size           = var.volume_size
    destination_type      = "volume"
    delete_on_termination = true
    source_type           = "image"
    uuid                  = data.openstack_images_image_v2.os.id
  }

  user_data = data.template_cloudinit_config.userdata.rendered
}

resource "openstack_compute_keypair_v2" "rdb-keypair" {
  name       = "${var.dev_ssh_key_name}-rdb-dev"
  public_key = var.dev_ssh_key
} 

resource "openstack_compute_secgroup_v2" "rdb-security-group" {
  name        = "rdb-security-group"
  description = "This defines the ports that we have decided to open."

  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 443
    to_port     = 443
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 3000
    to_port     = 3000
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 4000
    to_port     = 4000
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}
