# Practice foreman for Session 18: Jenkins LTS (Java 21), Maven, Git, the AWS CLI, and the plugins used here.
FROM jenkins/jenkins:lts-jdk21
USER root
RUN apt-get update && apt-get install -y --no-install-recommends maven git python3 python3-venv curl \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/awscli && /opt/awscli/bin/pip install --no-cache-dir -q awscli \
    && ln -s /opt/awscli/bin/aws /usr/local/bin/aws \
    && git config --system --add safe.directory '*'   # practice only: mounted repos belong to your own user
USER jenkins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
COPY jenkins.yaml /casc/jenkins.yaml
ENV CASC_JENKINS_CONFIG=/casc/jenkins.yaml
# Practice shortcuts: skip the setup wizard; allow a Git repository given as a local folder path;
# let the Git "bell" (/git/notifyCommit) be rung without an access token. By default Jenkins refuses it with HTTP 401, which is the safe setting. Never relax this on a real server.
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true -Dhudson.plugins.git.GitStatus.NOTIFY_COMMIT_ACCESS_CONTROL=disabled-for-polling"
