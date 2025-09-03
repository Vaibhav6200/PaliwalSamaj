sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install openjdk-11-jre

wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key |
  sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
/etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins


sudo systemctl daemon-reload
sudo systemctl start jenkins

# NOTE: if we get error that jenkins start failed, then upgrade java version to java17 and restart jenkins
sudo systemctl restart jenkins


sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl enable jenkins
sudo systemctl status jenkins

