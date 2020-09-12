floating_ip = "206.12.120.8"
environment = "staging"
os_auth_url= "https://cedar.cloud.computecanada.ca:5000"
os_tenant_id = "baf14655f3b544278b6c54b0e393732d"
os_tenant_name = "CCInternal-ikenna"
volume_size = 150
os_cloud = "rdb-on-cedar"
image = {
  id = "478a7fe3-aec3-4adf-b1b7-d69f284453b6"
  name = "CentOS-8-x64-2020-02"
}
flavor = {
  id = "1d3f7505-c1cd-4aab-8605-bf0093475a89"
  name = "p1-1.5gb"
}
pool = {
  id = "8ccaccf4-eb33-44b7-ac5a-49edde7ba4ab"
  name = "CCInternal-ikenna-network"
}
private = {
  id = "8ccaccf4-eb33-44b7-ac5a-49edde7ba4ab"
  name = "CCInternal-ikenna-network"
}
