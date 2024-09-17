FROM registry.access.redhat.com/ubi9/python-311:latest

# Install terraform & oh-my-zsh
USER root
RUN yum install -y yum-utils && \
    yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo && \
    yum -y install terraform zsh && \
    wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
USER 1001

# Install poetry
RUN pip install poetry 
#&& \
#    poetry config virtualenvs.create false

#RUN pip install ipykernel -U --user --force-reinstall

COPY ./pyproject.toml /opt/app-root/src/pyproject.toml

#RUN poetry add ipykernel
#RUN pip install ipykernel -U --user --force-reinstall
# Set default shell to zsh
ENV SHELL /bin/zsh

# Create workspace dir used by VSCode
RUN mkdir /opt/app-root/src/workspace/

# Expose ports
EXPOSE 4000