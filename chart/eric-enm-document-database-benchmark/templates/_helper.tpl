{{- define "eric-enm-document-database-benchmark.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.version" -}}
{{- printf "%s" .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "eric-enm-document-database-benchmark.prometheus.port" -}}
9600
{{- end -}}

{{- define "eric-enm-document-database-benchmark.orchestrator.http.port" -}}
8080
{{- end -}}

{{- define "eric-enm-document-database-benchmark.prometheus.annotations" -}}
prometheus.io/scrape: "true"
prometheus.io/port: {{ include "eric-enm-document-database-benchmark.prometheus.port" . | quote }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.product.annotations" -}}
ericsson.com/product-name: "Document Database Benchmark"
ericsson.com/product-number: "CXD 174 1531"
ericsson.com/product-revision: {{ regexReplaceAll "(.*)[+|-].*" .Chart.Version "${1}" | quote }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.securityContext" -}}
allowPrivilegeEscalation: false
privileged: false
capabilities:
  drop:
      - ALL
readOnlyRootFilesystem: true
runAsNonRoot: true
{{- end }}

{{ define "eric-enm-document-database-benchmark.globals" }}
  {{- $globalDefaults := dict "cnivAgent" (dict "enabled" false) -}}
  {{- $globalDefaults := merge $globalDefaults (dict "cnivAgent" (dict "name" "eric-oss-cniv" )) -}}
  {{- $globalDefaults := merge $globalDefaults (dict "cnivAgent" (dict "port" "8080" )) -}}
  {{- $globalDefaults := merge $globalDefaults (dict "registry" (dict "url" "armdocker.rnd.ericsson.se" )) -}}
  {{ if .Values.global }}
    {{- mergeOverwrite $globalDefaults .Values.global | toJson -}}
  {{ else }}
    {{- $globalDefaults | toJson -}}
  {{ end }}
{{ end }}

{{- define "eric-enm-document-database-benchmark.orchestrator.registry.url" -}}
{{- $registry := .Values.imageCredentials.orchestrator.registry.url -}}
{{- if not (.Values.imageCredentials.orchestrator.registry.url) -}}
  {{- if .Values.global -}}
    {{- if .Values.global.registry -}}
      {{- if .Values.global.registry.url -}}
          {{- $registry = .Values.global.registry.url -}}
      {{- end }}
    {{- end }}
  {{- end }}
{{- end }}
{{- $registry -}}
{{- end }}

{{- define "eric-enm-document-database-benchmark.benchmark.registry.url" -}}
{{- $registry := .Values.imageCredentials.benchmark.registry.url -}}
{{- if not (.Values.imageCredentials.benchmark.registry.url) -}}
  {{- if .Values.global -}}
    {{- if .Values.global.registry -}}
      {{- if .Values.global.registry.url -}}
          {{- $registry = .Values.global.registry.url -}}
      {{- end }}
    {{- end }}
  {{- end }}
{{- end }}
{{- $registry -}}
{{- end }}

{{- define "eric-enm-document-database-benchmark.init-wait.registry.url" -}}
{{- $registry := .Values.imageCredentials.init_wait.registry.url -}}
{{- if not (.Values.imageCredentials.init_wait.registry.url) -}}
  {{- if .Values.global -}}
    {{- if .Values.global.registry -}}
      {{- if .Values.global.registry.url -}}
          {{- $registry = .Values.global.registry.url -}}
      {{- end }}
    {{- end }}
  {{- end }}
{{- end }}
{{- $registry -}}
{{- end }}

{{- define "eric-enm-document-database-benchmark.pullSecret" -}}
{{- $pullSecret := .Values.imageCredentials.pullSecret -}}
{{- if not (.Values.imageCredentials.pullSecret) -}}
    {{- if .Values.global -}}
        {{- if .Values.global.pullSecret -}}
            {{- $pullSecret = .Values.global.pullSecret -}}
        {{- end }}
    {{- end }}
{{- end }}
{{- $pullSecret -}}
{{- end }}

{{- define "eric-enm-document-database-benchmark.orchestrator.pullPolicy" -}}
{{- $pullPolicy := .Values.imageCredentials.orchestrator.registry.imagePullPolicy -}}
{{- if not (.Values.imageCredentials.orchestrator.registry.imagePullPolicy) -}}
    {{- if .Values.global -}}
        {{- if .Values.global.registry -}}
          {{- if .Values.global.registry.imagePullPolicy -}}
              {{- $pullPolicy = .Values.global.registry.imagePullPolicy -}}
          {{- end }}
        {{- end }}
    {{- end }}
{{- end }}
{{- $pullPolicy -}}
{{- end }}

{{- define "eric-enm-document-database-benchmark.benchmark.pullPolicy" -}}
{{- $pullPolicy := .Values.imageCredentials.benchmark.registry.imagePullPolicy -}}
{{- if not (.Values.imageCredentials.benchmark.registry.imagePullPolicy) -}}
    {{- if .Values.global -}}
        {{- if .Values.global.registry -}}
          {{- if .Values.global.registry.imagePullPolicy -}}
              {{- $pullPolicy = .Values.global.registry.imagePullPolicy -}}
          {{- end }}
        {{- end }}
    {{- end }}
{{- end }}
{{- $pullPolicy -}}
{{- end }}

{{- define "eric-enm-document-database-benchmark.init-wait.pullPolicy" -}}
{{- $pullPolicy := .Values.imageCredentials.init_wait.registry.imagePullPolicy -}}
{{- if not (.Values.imageCredentials.init_wait.registry.imagePullPolicy) -}}
    {{- if .Values.global -}}
        {{- if .Values.global.registry -}}
          {{- if .Values.global.registry.imagePullPolicy -}}
              {{- $pullPolicy = .Values.global.registry.imagePullPolicy -}}
          {{- end }}
        {{- end }}
    {{- end }}
{{- end }}
{{- $pullPolicy -}}
{{- end }}

{{- define "eric-enm-document-database-benchmark.pgbench.imageName" -}}
{{ include "eric-enm-document-database-benchmark.benchmark.registry.url" . }}/{{.Values.image.repoPath}}/eric-enm-document-database-benchmark-load-tester:{{.Values.image.pgbm.tag }}
{{- end -}}

{{- define "eric-enm-document-database-benchmark.results.imageName" -}}
{{ include "eric-enm-document-database-benchmark.orchestrator.registry.url" . }}/{{.Values.image.repoPath}}/eric-enm-document-database-benchmark-orchestrator:{{.Values.image.results.tag }}
{{- end -}}

{{- define "eric-enm-document-database-benchmark.eric-cniv-init-wait.imageName" -}}
{{ include "eric-enm-document-database-benchmark.init-wait.registry.url" . }}/{{.Values.image.repoPath}}/eric-cniv-init-wait:{{.Values.image.initWaitCNIV.tag }}
{{- end -}}

{{- define "eric-enm-document-database-benchmark.cnivAgent.enabled" -}}
{{- $g := fromJson (include "eric-enm-document-database-benchmark.globals" .) -}}
{{- $g.cnivAgent.enabled }}
{{- end -}}

{{- define "eric-enm-document-database-benchmark.cnivAgent.name" -}}
{{- $g := fromJson (include "eric-enm-document-database-benchmark.globals" .) -}}
{{- $g.cnivAgent.name }}
{{- end -}}

{{- define "eric-enm-document-database-benchmark.cnivAgent.port" -}}
{{- $g := fromJson (include "eric-enm-document-database-benchmark.globals" .) -}}
{{- $g.cnivAgent.port }}
{{- end -}}

{{- define "eric-enm-document-database-benchmark.common.labels" -}}
app.kubernetes.io/name: {{ $.Chart.Name }}
app.kubernetes.io/version: {{ include "eric-enm-document-database-benchmark.version" . }}
app.kubernetes.io/instance : {{ .Release.Name }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.pgbenchmark.labels" -}}
{{- include "eric-enm-document-database-benchmark.common.labels" . }}
app.kubernetes.io/component: {{ include "eric-enm-document-database-benchmark.name" . }}-load-tester
job-name: {{ include "eric-enm-document-database-benchmark.name" . }}-load-tester
{{- end }}

{{- define "eric-enm-document-database-benchmark.orchestrator.labels" -}}
{{- include "eric-enm-document-database-benchmark.common.labels" . }}
app.kubernetes.io/component: {{ include "eric-enm-document-database-benchmark.name" . }}
job-name: {{ $.Chart.Name }}
benchmarkname: {{ $.Chart.Name }}
{{- if .Values.global -}}
{{- if .Values.global.cnivAgent }}
{{- if .Values.global.cnivAgent.enabled }}
benchmarkgroup: {{ include "eric-enm-document-database-benchmark.labels.benchmarkGroup" . }}
{{- end }}
{{- end }}
{{- end }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.labels.benchmarkGroup" -}}
  {{- if .Values.global -}}
    {{- if .Values.global.cnivAgent }}
      {{- if .Values.global.cnivAgent.enabled }}
        {{- range $groupmap := .Values.global.sequence -}}
          {{- range $group,$benchmarks := $groupmap -}}
            {{- range $bench := $benchmarks }}
              {{- if eq $.Chart.Name $bench }}
                {{- $label := print $group -}}
                {{- $label | lower | trunc 54 | trimSuffix "-" -}}
              {{- end }}
            {{- end }}
          {{- end }}
        {{- end }}
      {{- end }}
    {{- end }}
  {{- else }}
    {{- $label := print "default" -}}
    {{- $label | lower | trunc 54 | trimSuffix "-" -}}
  {{- end }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.pgbench.configs" -}}
  {{- with (index .Values (.Values.environmentType ) "pgbench") }}
  pgbench:
    clients: {{ .clients }}
    time: {{ .time }}
    threads: {{ .threads }}
    scale_factor: {{ .scale_factor }}
    weight: {{ .weight }}
    filename: {{ .filename }}
    rate: {{ .rate }}
  {{- end }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.parallelExecutions" -}}
  {{- with (index .Values (.Values.environmentType ) ) }}
    {{ .parallelExecutions }}
  {{- end }}
{{- end }}

{{- define "eric-enm-document-database-benchmark.internalIPFamily" -}}
{{- if .Values.global }}
{{- if .Values.global.internalIPFamily }}
ipFamilies: [{{ .Values.global.internalIPFamily | quote }}]
ipFamilyPolicy: SingleStack
{{- else }}
ipFamilyPolicy: PreferDualStack
{{- end }}
{{- end }}
{{- end }}
