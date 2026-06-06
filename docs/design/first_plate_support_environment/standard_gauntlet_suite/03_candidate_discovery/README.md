# Candidate Discovery Design

## Purpose

This folder is for selecting downstream candidate schemas or towers from the
diagnostic/sweep stages.

## Starting Point

Counterpoint eventually needed explicit candidate manifests so downstream
training did not silently pick unusable or collapsed towers. PlateSupport should
inherit that discipline but define candidate eligibility in PlateSupport terms.

## Design Question

What makes a PlateSupport tower candidate eligible for training-health and
paired-comparison stages?
