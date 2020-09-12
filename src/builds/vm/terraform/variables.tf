variable "floating_ip" {
  type = string
  description = "This is the floating IP address that will be allocated to this VM post creation"
  default = "206.12.95.111"
}
variable "user_name" {
  type = string
  description = "This is ccdb username"
  default = "wgdev"
}
variable "password" {
  type = string
  description = "This is ccdb user password"
  
  validation {
    condition     = var.password != "" && length(var.password) > 0
    error_message = "The password can't be empty, set it with -var=\"password=<ccdb-user-password>\"."
  }
}
variable "os_cloud" {
  type = string
  description = "This is entry name given in ~/.config/openstack/clouds.yaml"
  default = "rdb-on-arbutus"
}
variable "os_auth_url" {
  type = string
  description = "This is openstack API endpoint"
  default = "https://arbutus.cloud.computecanada.ca:5000"
}
variable "os_tenant_id" {
  type = string
  description = "This is openstack tenant id"
  default = "080be08a94d34ea9acfcbf56ee7dc0d6"
}
variable "os_tenant_name" {
  type = string
  description = "This is openstack tenant name"
  default = "def-pjmann-covid19"
}
variable "vm_ssh_key_pub" {
  type = string
  description = "This is the path the user's id_rsa.pub"
}
variable "vm_ssh_key_priv" {
  type = string
  description = "This is the path the user's id_rsa"
}
variable "dev_ssh_key" {
  type = string
  description = "This is the content of the id_rsa.pub file"
}
variable "dev_ssh_key_name" {
  type = string
  description = "This is the name given to the SSH key"
}
variable "environment" {
  type = string
  description = "This is the name to the environment, which serves as an identifier. Example: development | staging | production"
  default = "development"
}
variable "image" {
  type = object({
    id = string
    name = string
  })
  description = "This is the name and id of the choosen OS image"
  default = {
    id = "80ceebef-f9aa-462e-a793-d3c1cf96123b"
    name = "CentOS-8-x64-2019-11"
  }
}
variable "volume_size" {
  type = string
  description = "This is the size of the vm's volume"
  default = 25000
}
# Default flavor to use for instances
variable "flavor" {
  type = object({
    id = string
    name = string
  })
  description = "This is the name and id of the choosen pre-defined system flavor"
	default = {
    id = "17190760-f7a5-4d0e-b874-e7a22d8d57fe"
    name = "p4-4gb"
  }
}
variable "pool" {
  type = object({
    id = string
    name = string
  })
  description = "This is the name and id of the choosen Network pool. Network name for floating IP addresses (must correspond to external_gateway)"
	default = {
    id = "35f33a22-e091-4a00-9a01-39af3964b6be"
    name = "def-pjmann-covid19-network"
  }
}
variable "private" {
  type = object({
    id = string
    name = string
  })
  description = "This is the name and id of the choosen private network"
    default = {
      id = "35f33a22-e091-4a00-9a01-39af3964b6be"
      name = "def-pjmann-covid19-network"
    }
}
