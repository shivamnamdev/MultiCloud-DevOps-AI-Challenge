def call(Map cfg = [:]) {
  def status = cfg.status ?: 'UNKNOWN'
  def line = "[${status}] ${env.JOB_NAME} #${env.BUILD_NUMBER} ${env.BUILD_URL}"
  echo line
  if (cfg.topic) {
    sh "aws sns publish --topic-arn '${cfg.topic}' --message '${line}'"
  }
}
