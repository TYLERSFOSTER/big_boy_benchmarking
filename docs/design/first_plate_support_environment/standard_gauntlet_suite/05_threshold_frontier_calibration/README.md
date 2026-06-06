# Threshold Frontier Calibration Design

## Purpose

This folder is for PlateSupport threshold or frontier calibration.

## Starting Point

Counterpoint showed that a comparison threshold can be too weak, too strong, or
behaviorally impossible under the episode/window budget. PlateSupport reward
scale and stopping behavior are different, so thresholds must be calibrated from
PlateSupport evidence.

## Design Question

What threshold, success, or frontier signal should define "solving" or
meaningful progress for PlateSupport under a small but real budget?
