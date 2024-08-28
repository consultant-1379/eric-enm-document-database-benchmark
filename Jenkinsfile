#!/usr/bin/env groovy

/* IMPORTANT:
 *
 * In order to make this pipeline work, the following configuration on Jenkins is required:
 * - slave with a specific label (see pipeline.agent.label below)
 * - credentials plugin should be installed and have the secrets with the following names:
 *   + lciadm100credentials (token to access Artifactory)
 */

def defaultBobImage = 'armdocker.rnd.ericsson.se/sandbox/adp-staging/adp-cicd/bob.2.0:1.7.0-83'
def bob = new BobCommand()
        .bobImage(defaultBobImage)
        .envVars([ISO_VERSION: '${ISO_VERSION}'])
        .needDockerSocket(true)
        .toString()
def failedStage = ''
def GIT_COMMITTER_NAME = 'enmadm100'
def GIT_COMMITTER_EMAIL = 'enmadm100@ericsson.com'

pipeline {
    agent {
        label 'Cloud-Native'
    }
    parameters {
        string(name: 'ISO_VERSION', description: 'The ENM ISO version (e.g. 1.65.77)')
        string(name: 'SPRINT_TAG', description: 'Tag for GIT tagging the repository after build')
    }
    stages {
        stage('Clean') {
            steps {
                sh("${bob} clean")
            }
        }
        stage('Set current working directory') {
            steps {
                script {
                    sh "${bob} set-working-directory"
                }
            }
        }
        stage('Inject Credential Files') {
            steps {
                withCredentials([file(credentialsId: 'lciadm100-docker-auth', variable: 'dockerConfig')]) {
                    sh "install -m 600 ${dockerConfig} ${HOME}/.docker/config.json"
                }
            }
        }
        stage('Checkout Cloud-Native SG Git Repository') {
            steps {
                git branch: 'master',
                    credentialsId: 'enmadm100_private_key',
                     url: '${GERRIT_MIRROR}/OSS/ENM-Parent/SQ-Gate/com.ericsson.oss.containerisation/eric-enm-document-database-benchmark'
                sh '''
                    git remote set-url origin --push ${GERRIT_CENTRAL}/OSS/ENM-Parent/SQ-Gate/com.ericsson.oss.containerisation/eric-enm-document-database-benchmark
                '''
            }
        }
        stage('Helm Dep Up') {
            steps {
                sh "${bob} helm-dep-up"
            }
            post {
                failure {
                    script {
                        failedStage = env.STAGE_NAME
                    }
                }
            }
        }
        stage('Build & Push Docker Images') {
            steps {
                sh "${bob} get-commit-hash"
                sh "${bob} prepare-release-build"
                sh "${bob} prepare-docker-image-paths"
                sh "${bob} build-and-push-base-image"
                sh "${bob} build-and-push-images"
            }
            post {
                failure {
                    script {
                        failedStage = env.STAGE_NAME
                    }
                }
            }
        }
        stage('Build & Push Helm Chart') {
            steps {
                sh "${bob} build-helm"
                sh "${bob} push-helm"
            }
            post {
                failure {
                    script {
                        failedStage = env.STAGE_NAME
                    }
                }
            }
        }
        stage('Helm Lint') {
            steps {
                sh "${bob} lint-helm-artefact"
            }
            post {
                failure {
                    script {
                        failedStage = env.STAGE_NAME
                    }
                }
            }
        }
        stage("Vulnerability Analysis"){
            steps{
                parallel(
                    "Kubeaudit": {
                        script {
                            sh "${bob} kube-audit"
                            sh "echo -n ' --kubeaudit-reports build/va-reports/kube-audit-report' >>.bob/var.va-report-arguments"
                        }
                    },
                    "Kubsec": {
                        script {
                            sh "mkdir config && touch config/kubesec_config.yaml"
                            sh 'FILE=jenkins/cnivFiles/va/kubesec_config.yaml && git archive --remote=${GERRIT_MIRROR}/OSS/ENM-Parent/SQ-Gate/com.ericsson.oss.containerisation/cniv-ci-pipeline HEAD "$FILE" | tar -xO "$FILE" >  config/kubesec_config.yaml'
                            sh "${bob} kubesec-scan"
                            sh "echo -n ' --kubesec-reports build/va-reports/kubesec-reports' >>.bob/var.va-report-arguments"
                        }
                    },
                    "Trivy": {
                        script {
                            sh "${bob} trivy-inline-scan"
                            sh "echo -n ' --trivy-reports build/va-reports/trivy-reports' >>.bob/var.va-report-arguments"
                        }
                    },
                    "Anchore-Grype": {
                        script {
                            sh "${bob} anchore-grype-scan"
                            sh "echo -n ' --anchore-reports build/va-reports/anchore-reports' >>.bob/var.va-report-arguments"
                        }
                    }
                )
            }
        }
        stage("Xray Scan") {
            steps {
                sh "${bob} fetch-xray-report"
                sh "echo -n ' --xray build/va-reports/xray-reports/xray_report.json' >>.bob/var.va-report-arguments"
            }
        }
        stage('Overall VA Report') {
            steps {
                script {
                    sh "${bob} generate-VA-report-V2 || true"
                }
            }
        }
    }
    post {
        always{
            archiveArtifacts 'helmlint-artefact.log'
            archiveArtifacts artifacts: 'Vulnerability_Report_2.0.md', allowEmptyArchive: true
            archiveArtifacts allowEmptyArchive: true, artifacts: 'build/va-reports/xray-reports/xray_report.json'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'build/va-reports/xray-reports/raw_xray_report.json'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'build/va-reports/trivy-reports/**.*,  trivy_metadata.properties,' +
                    ' build/va-reports/kube-audit-report/**/*, build/va-reports/kubesec-reports/*, build/va-reports/anchore-reports/**.*'
        }
        success {
            script {
                sh '''
                    set +x
                    echo "success"
                '''
            }
        }
        failure {
           script {
               sh '''
                   echo "Failed"
               '''
           }
        }
    }
}

// More about @Builder: http://mrhaki.blogspot.com/2014/05/groovy-goodness-use-builder-ast.html
import groovy.transform.builder.Builder
import groovy.transform.builder.SimpleStrategy

@Builder(builderStrategy = SimpleStrategy, prefix = '')
class BobCommand {
    def bobImage = 'bob.2.0:latest'
    def envVars = [:]
    def needDockerSocket = false
    def rulesetFile = 'ruleset2.0.yaml'

    String toString() {
        def env = envVars
                .collect({ entry -> "-e ${entry.key}=\"${entry.value}\"" })
                .join(' ')

        def cmd = """\
            |docker run
            |--init
            |--rm
            |--workdir \${PWD}
            |--user \$(id -u):\$(id -g)
            |-v \${PWD}:\${PWD}
            |-v /etc/group:/etc/group:ro
            |-v /etc/passwd:/etc/passwd:ro
            |-v \${HOME}/.m2:\${HOME}/.m2
            |-v \${HOME}/.docker:\${HOME}/.docker
            |${needDockerSocket ? '-v /var/run/docker.sock:/var/run/docker.sock' : ''}
            |${env}
            |\$(for group in \$(id -G); do printf ' --group-add %s' "\$group"; done)
            |--group-add \$(stat -c '%g' /var/run/docker.sock)
            |${bobImage}
            |-r ${rulesetFile}
            |"""
        return cmd
                .stripMargin()           // remove indentation
                .replace('\n', ' ')      // join lines
                .replaceAll(/[ ]+/, ' ') // replace multiple spaces by one
    }
}