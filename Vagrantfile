# -*- mode: ruby -*- vi: set ft=ruby :


Vagrant.configure(2) do |config|
  config.vm.define "ubuntu", primary: true do |ubuntu|
    ubuntu.vm.box = "ubuntu/trusty64"
    ubuntu.vm.provision :shell, :path => "dev/vagrant-ubuntu-bootstrap.sh", :privileged => false
  end

  config.ssh.insert_key = false

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
end
