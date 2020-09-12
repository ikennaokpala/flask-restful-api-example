data "openstack_images_image_v2" "os" {
  name        = var.image["name"]
  most_recent = true
}

data "openstack_networking_floatingip_v2" "floating_ip" {
  address = var.floating_ip
} 

data "template_file" "cloud-init" {
  template = "${file("${path.module}/config/templates/cloud-init.yaml")}"

  vars = {
    vm_ssh_key_priv = var.vm_ssh_key_priv
    vm_ssh_key_pub = var.vm_ssh_key_pub
  }
}

data "template_cloudinit_config" "userdata" {
  part {
    content = data.template_file.cloud-init.rendered
  }

  part {
    filename     = "extra.sh"
    content_type = "text/cloud-config"
    content      = ""
    merge_type   = "list(append)+dict(recurse_array)+str()"
  }
}
