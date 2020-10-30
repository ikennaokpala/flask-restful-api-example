data "openstack_images_image_v2" "os" {
  name        = var.image["name"]
  most_recent = true
}

data "openstack_networking_floatingip_v2" "floating_ip" {
  address = var.floating_ip
}

locals { 
  salted = sha256(bcrypt(replace(timestamp(), "/[-| |T|Z|:]/", "")))

  pg_db_password = substr(local.salted, 13, 21)
  pg_db_api_password = substr(local.salted, 22, 30)
}

data "template_file" "cloud-init" {
  template = "${file("${path.module}/config/templates/cloud-init.yaml")}"

  vars = {
    rdb_domain = var.domain
    rdb_domains = var.domains
    pg_db_user = var.pg_db_user
    pg_db_name = var.pg_db_name
    pg_db_port = var.pg_db_port
    pg_db_domain = var.pg_db_domain
    pg_db_protocol = var.pg_db_protocol
    vm_ssh_key_pub = var.vm_ssh_key_pub
    vm_ssh_key_priv = var.vm_ssh_key_priv
    cors_clients = "${var.domain},${var.domains}"
    pg_db_password = local.pg_db_password
    pg_db_api_password = local.pg_db_api_password
    pdb_postgresql_data_path = var.pdb_postgresql_data_path
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
