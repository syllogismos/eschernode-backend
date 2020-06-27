`bash Miniconda3-latest-Linux-x86_64.sh`
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

#To export environment file
activate <environment-name>
conda env export > <environment-name>.yml

#For other person to use the environment
conda env create -f <environment-name>.yml
