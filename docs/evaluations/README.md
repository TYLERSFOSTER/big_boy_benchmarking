# Evaluations

Checked-in files in this folder describe how to read evaluation docs and which
claim boundaries apply.

Generated evaluation docs should be written under the artifact root by default:

```text
<artifact-root>/evaluations/<evaluation-id>/docs/
```

Do not commit generated Markdown that contains machine-local artifact paths.
Use `<artifact-root>` placeholders in checked-in docs unless the repo is
intentionally recording a durable artifact location.
