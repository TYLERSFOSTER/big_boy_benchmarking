# Security Policy

## Supported Versions

The source-first public beta supports the current `main` branch and the planned
`v0.1.0-beta.1` tag once that tag exists.

## Reporting A Vulnerability

Until a dedicated security contact is published, use the GitHub repository's
private vulnerability reporting surface if available. If that is not available,
open a minimal public issue that does not include exploit details and ask for a
private follow-up channel.

## Artifact And Provenance Caution

Evaluation artifacts can contain local provenance, run configuration, dependency
state, and generated traces. Public release preparation removes machine-local
paths from tracked public surfaces and externalizes raw artifact trees, but
future artifact additions should still be reviewed before publication.
