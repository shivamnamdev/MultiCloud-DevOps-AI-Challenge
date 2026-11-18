# Practice foreman: Jenkins LTS (Java 21) with Maven and Git, plus the plugins this session uses.
FROM jenkins/jenkins:lts-jdk21
USER root
RUN apt-get update && apt-get install -y --no-install-recommends maven git \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory '*'   # practice only: the mounted repo is owned by your own user
USER jenkins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
COPY jenkins.yaml /casc/jenkins.yaml
ENV CASC_JENKINS_CONFIG=/casc/jenkins.yaml
# Practice shortcuts: skip the setup wizard, and allow a Git repository given as a local folder path.
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true"
